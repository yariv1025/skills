# I9 – Lack of Physical Hardening

## Summary

Physical interfaces (e.g. UART, JTAG) or lack of tamper detection allow local attackers to extract secrets or modify device.

## Prevention

- Disable or protect debug interfaces in production; use tamper detection and secure boot. Restrict physical access to sensitive components where feasible.

## Testing

- Inspect physical interfaces; verify debug disable and secure boot; test tamper response.
