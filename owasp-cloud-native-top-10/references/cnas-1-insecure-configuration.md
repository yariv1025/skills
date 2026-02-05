# CNAS-1 – Insecure cloud, container or orchestration configuration

## Summary

Publicly open storage, improper permissions, containers running as root, insecure IaC. Misconfiguration is a leading cause of cloud-native incidents.

## Prevention

Follow hardening guides for cloud, container, and orchestrator. Use policy-as-code and admission; scan config; principle of least privilege.

## Examples

### Wrong - Public S3 bucket

```terraform
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id
  # All set to false - bucket is public!
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
```

### Right - Private S3 bucket with encryption

```terraform
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

### Wrong - Bloated container running as root

```dockerfile
FROM ubuntu:latest

# Running as root by default
RUN apt-get update && apt-get install -y \
    python3 python3-pip curl vim wget netcat \
    && pip3 install -r requirements.txt

COPY . /app
WORKDIR /app
CMD ["python3", "app.py"]
```

### Right - Minimal hardened container

```dockerfile
# Use distroless or minimal base
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

FROM gcr.io/distroless/python3-debian12
WORKDIR /app

# Copy only what's needed
COPY --from=builder /app/deps /app/deps
COPY app.py .

# Run as non-root
USER nonroot:nonroot

ENV PYTHONPATH=/app/deps
CMD ["app.py"]
```

### Wrong - Overly permissive IAM role

```terraform
resource "aws_iam_role_policy" "lambda" {
  name = "lambda-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"           # Full AWS access!
      Resource = "*"
    }]
  })
}
```

### Right - Least privilege IAM

```terraform
resource "aws_iam_role_policy" "lambda" {
  name = "lambda-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:GetItem", "dynamodb:PutItem"]
        Resource = aws_dynamodb_table.users.arn
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.config.arn}/*"
      }
    ]
  })
}
```

### Cloud-native hardening checklist

| Component | Check |
|-----------|-------|
| S3/GCS/Blob | Block public access, enable encryption |
| Containers | Non-root, minimal base, read-only fs |
| IAM roles | Least privilege, no wildcards |
| Network | Private subnets, security groups |
| Secrets | Use secrets manager, not env vars |
| Logging | Enable CloudTrail/audit logs |

## Testing

Scan config and IaC; check for public resources and excessive permissions; verify runtime settings.
