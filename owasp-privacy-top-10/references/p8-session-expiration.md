# P8 – Missing or Insufficient Session Expiration

## Summary

Sessions that do not expire properly. Abandoned devices or stolen tokens retain access; increases exposure of account and data.

## Prevention

Set appropriate session timeout (absolute and idle); invalidate on logout and password change; use secure cookie flags and token storage; support "logout everywhere."

## Testing

Verify session timeout and logout behavior; test token invalidation; check cookie flags.
