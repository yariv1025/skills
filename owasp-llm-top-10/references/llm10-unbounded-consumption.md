# LLM10 – Unbounded Consumption

## Summary

Lack of rate limiting and cost controls leads to DoS, denial-of-wallet, or model extraction via excessive queries. Resource and cost abuse.

## Prevention

- Apply rate limits, quotas, and cost controls per user/tenant. Detect and throttle abuse; protect against extraction and automated scraping; monitor usage.

## Testing

- Test rate limits and quotas; attempt cost exhaustion and extraction; verify monitoring and alerting.
