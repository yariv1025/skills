# A03:2021 – Injection

## Summary

Injection flaws occur when untrusted data is sent to an interpreter (SQL, NoSQL, OS, LDAP, template engine, etc.) as part of a command or query. Attackers can execute unintended commands or access data. Very common and high impact.

## Key CWEs

- CWE-79 Cross-site Scripting (XSS)
- CWE-89 SQL Injection
- CWE-78 OS Command Injection
- CWE-917 Expression Language Injection
- CWE-94 Code Injection

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A03_2021-Injection/) for the full list.*

## Root Causes / Triggers

- Concatenating or interpolating user input into commands, queries, or templates.
- Missing or weak input validation and output encoding.
- Over-privileged database or process accounts.

## Prevention Checklist

- Use parameterized queries or prepared statements for all SQL/NoSQL; never build queries from string concatenation.
- Validate input (type, length, format) and use allowlists where possible.
- Encode output for the correct context (HTML, URL, JavaScript, etc.) to prevent XSS.
- Use safe APIs that avoid command/shell invocation; if unavoidable, strict allowlists and minimal privilege.
- Apply principle of least privilege for DB and process accounts.

## Secure Patterns

- **SQL:** Prepared statements with bound parameters: `SELECT * FROM users WHERE id = ?` and pass ID as parameter.
- **Output encoding:** Use framework or library encoding for the target context (e.g. HTML entity encoding for HTML body).
- **Templates:** Use template engines that auto-escape by default; avoid raw inclusion of user input.

## Examples

### Wrong - SQL injection via string concatenation

```python
def get_user(username: str):
    # Attacker input: ' OR '1'='1' --
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # Executes: SELECT * FROM users WHERE username = '' OR '1'='1' --'
    return cursor.fetchone()
```

### Right - Parameterized query

```python
def get_user(username: str):
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    return cursor.fetchone()
```

### Right - Using ORM (SQLAlchemy)

```python
def get_user(username: str):
    # ORM handles parameterization automatically
    return User.query.filter_by(username=username).first()
```

### Wrong - XSS via unescaped output

```python
from flask import Flask, request
app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    # User input rendered directly - XSS vulnerability
    return f"<h1>Results for: {query}</h1>"
```

### Right - HTML encoding

```python
import html
from flask import Flask, request

@app.route("/search")
def search():
    query = request.args.get("q", "")
    safe_query = html.escape(query)
    return f"<h1>Results for: {safe_query}</h1>"
```

### Right - Using template engine with auto-escape

```python
from flask import render_template

@app.route("/search")
def search():
    query = request.args.get("q", "")
    # Jinja2 auto-escapes by default
    return render_template("search.html", query=query)
```

### Wrong - OS command injection

```python
import os

def ping_host(host: str):
    # Attacker input: 127.0.0.1; rm -rf /
    os.system(f"ping -c 1 {host}")
```

### Right - Avoid shell, use subprocess with list

```python
import subprocess
import re

def ping_host(host: str):
    # Validate input
    if not re.match(r'^[\w.-]+$', host):
        raise ValueError("Invalid hostname")
    # Use list args - no shell interpretation
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True
    )
    return result.stdout
```

### Context-aware encoding table

| Context | Encoding Method | Example |
|---------|-----------------|---------|
| HTML body | HTML entity encode | `&lt;script&gt;` |
| HTML attribute | HTML attribute encode + quote | `value="&quot;data&quot;"` |
| JavaScript string | JavaScript escape | `\x3cscript\x3e` |
| URL parameter | URL encode | `%3Cscript%3E` |
| CSS | CSS escape | `\3c script\3e` |

## Testing / Detection

- SAST for concatenation into queries/commands and missing encoding.
- DAST/injection testing (SQLi, XSS, command injection) with fuzzing and payloads.
- Code review for all sinks that process user input.
