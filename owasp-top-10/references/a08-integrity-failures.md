# A08:2021 – Software and Data Integrity Failures

## Summary

Failures related to software and data integrity include insecure deserialization, unsigned or unverified pipelines and updates, and supply chain compromise. Trust in build and update process without verification is a core issue.

## Key CWEs

- CWE-829 Inclusion of Functionality from Untrusted Control Sphere
- CWE-494 Download of Code Without Integrity Check
- CWE-502 Deserialization of Untrusted Data
- CWE-915 Improperly Controlled Modification of Dynamically-Determined Object Attributes

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/) for the full list.*

## Root Causes / Triggers

- Deserializing untrusted data without validation or type restriction (leading to RCE or abuse).
- CI/CD pipelines that do not verify artifact integrity or that run untrusted code.
- Updates or plugins installed without signature or integrity checks.
- Reliance on untrusted sources (e.g. unverified package repos).

## Prevention Checklist

- Do not deserialize untrusted data; use safe formats (e.g. JSON) and validate schema; restrict types if deserialization is required.
- Sign and verify artifacts in the pipeline; verify integrity before deployment.
- Use signed updates and verify signatures; secure the update mechanism.
- Maintain integrity of build environment and dependencies (see A06, supply chain).

## Secure Patterns

- **Deserialization:** Prefer data formats that do not allow object injection; if using serialization, use allowlists and minimal types; never deserialize from user input without strict control.
- **Pipeline:** Sign builds (e.g. attestations); verify before deploy; least privilege for pipeline identities.
- **Updates:** Verify signature or hash from a trusted source before applying.

## Examples

### Wrong - Insecure deserialization

```python
import pickle

@app.route("/load", methods=["POST"])
def load_data():
    # DANGER: Pickle can execute arbitrary code
    data = pickle.loads(request.data)
    return process(data)
```

### Right - Use safe data format with schema validation

```python
import json
from pydantic import BaseModel, ValidationError

class UserData(BaseModel):
    name: str
    email: str
    age: int

@app.route("/load", methods=["POST"])
def load_data():
    try:
        # JSON is safe - no code execution
        raw = json.loads(request.data)
        # Validate against schema
        data = UserData(**raw)
        return process(data)
    except (json.JSONDecodeError, ValidationError) as e:
        return {"error": "Invalid data"}, 400
```

### Wrong - No integrity check on updates

```python
def auto_update():
    # Downloads and runs without verification
    update = requests.get("http://example.com/update.zip")
    extract_and_install(update.content)
```

### Right - Verify signature before update

```python
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def auto_update():
    # Download update and signature
    update = requests.get("https://example.com/update.zip")
    signature = requests.get("https://example.com/update.zip.sig")
    
    # Verify signature with vendor's public key
    try:
        VENDOR_PUBLIC_KEY.verify(
            signature.content,
            update.content,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception:
        raise SecurityError("Update signature verification failed")
    
    extract_and_install(update.content)
```

### Wrong - Unsigned CI/CD artifacts

```yaml
# GitHub Actions - no artifact signing
jobs:
  build:
    steps:
      - run: docker build -t myapp .
      - run: docker push myapp:latest  # No signature
```

### Right - Signed container images

```yaml
# GitHub Actions with Cosign signing
jobs:
  build:
    steps:
      - run: docker build -t myapp .
      - name: Sign image with Cosign
        run: |
          cosign sign --key cosign.key \
            myapp@$(docker inspect --format='{{.Id}}' myapp)
      - run: docker push myapp:latest
```

### Deserialization safety table

| Format | Safe? | Notes |
|--------|-------|-------|
| JSON | Yes | No code execution, use with schema validation |
| XML | Caution | Disable external entities (XXE) |
| YAML | Caution | Use safe_load(), not load() |
| Pickle (Python) | No | Arbitrary code execution |
| Java Serialization | No | Arbitrary code execution |
| PHP serialize | No | Object injection possible |

## Testing / Detection

- SAST for deserialization of user-controlled data; review use of dangerous APIs.
- Verify pipeline signing and verification; test update integrity checks.
- Supply chain and dependency verification (see A06).
