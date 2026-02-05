# API6:2023 – Unrestricted Access to Sensitive Business Flows

## Summary

APIs expose business flows (e.g. signup, checkout, booking) without protection against excessive or automated use. Enables scalping, fake account creation, inventory abuse, or competitive scraping.

## Key CWEs

- CWE-799 Improper Control of Interaction Frequency
- CWE-837 Improper Enforcement of a Single, Unique Action

## Root Causes

- No anti-automation or bot detection; no limits on high-value or abuse-prone flows.
- Business logic not designed for adversarial use.

## Prevention Checklist

- Apply rate limiting and anti-automation (e.g. CAPTCHA, behavior analysis) to sensitive flows.
- Require step-up auth or additional verification for high-value actions.
- Monitor for abuse patterns; limit bulk or automated access.

## Secure Patterns

- Identify sensitive business flows and protect with rate limits, quotas, and optional CAPTCHA or challenge.
- Use idempotency keys where appropriate to prevent duplicate submissions while allowing retries.

## Examples

### Wrong - Unprotected checkout flow

```python
@app.post("/api/checkout")
def checkout():
    # No rate limiting, no anti-bot - scalpers can buy all inventory
    cart = get_cart(request.state.user.id)
    order = create_order(cart)
    return {"order_id": order.id}
```

### Right - Protected business flow

```python
from slowapi import Limiter

limiter = Limiter(key_func=lambda r: r.state.user.id)

@app.post("/api/checkout")
@limiter.limit("3/minute")  # Rate limit per user
def checkout(captcha_response: str = None):
    user = request.state.user
    
    # Verify CAPTCHA for high-value transactions
    cart = get_cart(user.id)
    if cart.total > 500:
        if not verify_captcha(captcha_response):
            raise HTTPException(400, "CAPTCHA verification required")
    
    # Check for suspicious patterns
    recent_orders = get_recent_orders(user.id, minutes=60)
    if len(recent_orders) > 5:
        flag_for_review(user.id)
        raise HTTPException(429, "Too many orders, please contact support")
    
    order = create_order(cart)
    return {"order_id": order.id}
```

### Wrong - Account creation without limits

```python
@app.post("/api/signup")
def signup(email: str, password: str):
    # Bot can create thousands of fake accounts
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"user_id": user.id}
```

### Right - Anti-automation on signup

```python
@app.post("/api/signup")
@limiter.limit("5/hour")  # Per IP
def signup(email: str, password: str, captcha_response: str):
    # Verify CAPTCHA
    if not verify_captcha(captcha_response):
        raise HTTPException(400, "Invalid CAPTCHA")
    
    # Check for disposable email
    if is_disposable_email(email):
        raise HTTPException(400, "Disposable emails not allowed")
    
    # Check IP reputation (optional)
    if is_suspicious_ip(request.client.host):
        require_additional_verification()
    
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"user_id": user.id}
```

### Right - Idempotency for payment flows

```python
@app.post("/api/payment")
def process_payment(idempotency_key: str, amount: int):
    # Check if this request was already processed
    existing = Payment.query.filter_by(idempotency_key=idempotency_key).first()
    if existing:
        return {"payment_id": existing.id, "status": existing.status}
    
    # Process new payment
    payment = Payment(
        idempotency_key=idempotency_key,
        amount=amount,
        user_id=request.state.user.id
    )
    process_with_provider(payment)
    db.session.add(payment)
    db.session.commit()
    return {"payment_id": payment.id, "status": payment.status}
```

### Sensitive flows to protect

| Flow | Protection |
|------|------------|
| Checkout/Purchase | Rate limit, CAPTCHA for high value |
| Account creation | CAPTCHA, email verification |
| Password reset | Rate limit, token expiry |
| Ticket booking | Rate limit, queue system |
| API key generation | Rate limit, approval workflow |
| Bulk export | Rate limit, async processing |

## Testing

- Automate sensitive flows and check for detection/blocking; test rate limits and step-up auth.
