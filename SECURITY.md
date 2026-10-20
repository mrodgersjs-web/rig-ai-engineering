# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 0.2.x | Yes |
| < 0.2 | No |

## Reporting

Email **security@rodgersintelligence.com** with:

- affected path or command
- impact
- proof of concept (non-destructive)

Do not open a public issue for secrets or exploitable bugs.

## Secrets

- Never commit `.env`, cookies, tokens, private keys, or customer data.
- Rotate any credential that may have been exposed.
- This package sends nothing anywhere: scoring is local regex and string work.
