# SL1 – Injection (Serverless)

## Summary

Event data (e.g. API body, queue message) used unsafely in queries, commands, or downstream services. Validate and sanitize all event input.

## Prevention

Use parameterized queries; validate event schema; allowlist inputs. Never concatenate event data into commands or queries.

## Examples

### Wrong - SQL injection in Lambda

```python
import json

def handler(event, context):
    user_id = event.get("queryStringParameters", {}).get("user_id")
    
    # DANGER: Direct string interpolation
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    
    # user_id = "' OR '1'='1" returns all users
    result = execute_query(query)
    return {"statusCode": 200, "body": json.dumps(result)}
```

### Right - Parameterized query

```python
import json

def handler(event, context):
    user_id = event.get("queryStringParameters", {}).get("user_id")
    
    # Validate input
    if not user_id or not user_id.isalnum():
        return {"statusCode": 400, "body": "Invalid user_id"}
    
    # Parameterized query
    query = "SELECT * FROM users WHERE id = :user_id"
    params = [{"name": "user_id", "value": {"stringValue": user_id}}]
    
    result = rds_client.execute_statement(
        resourceArn=DB_ARN,
        secretArn=SECRET_ARN,
        sql=query,
        parameters=params
    )
    return {"statusCode": 200, "body": json.dumps(result)}
```

### Wrong - Command injection from S3 event

```python
import subprocess

def handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    
    # DANGER: Filename could be "file.txt; rm -rf /"
    subprocess.run(f"process-file s3://{bucket}/{key}", shell=True)
```

### Right - Safe subprocess without shell

```python
import subprocess
import re
import os

def handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    
    # Validate filename pattern
    if not re.match(r'^[\w\-./]+$', key):
        raise ValueError("Invalid key format")
    
    # Download file first, then process
    local_path = f"/tmp/{os.path.basename(key)}"
    s3.download_file(bucket, key, local_path)
    
    # No shell=True, list of arguments
    subprocess.run(["process-file", local_path], check=True)
```

### Right - Schema validation for event input

```python
from pydantic import BaseModel, field_validator
import json

class UserInput(BaseModel):
    user_id: str
    action: str
    
    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v):
        if not v.isalnum() or len(v) > 36:
            raise ValueError("Invalid user_id")
        return v
    
    @field_validator("action")
    @classmethod
    def validate_action(cls, v):
        allowed = {"view", "edit", "delete"}
        if v not in allowed:
            raise ValueError(f"Action must be one of {allowed}")
        return v

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        data = UserInput(**body)
    except Exception as e:
        return {"statusCode": 400, "body": str(e)}
    
    # Safe to use validated data
    process_action(data.user_id, data.action)
```

### Serverless injection vectors

| Event Source | Risk | Mitigation |
|--------------|------|------------|
| API Gateway body | SQL, NoSQL, command injection | Validate schema, parameterize |
| S3 object key | Command injection, path traversal | Validate pattern, sanitize |
| SNS/SQS message | All injection types | Schema validation |
| DynamoDB Stream | Trust boundary - validate anyway | Validate before downstream use |

## Testing

Fuzz event payloads; test for injection into DB, OS, or downstream APIs.
