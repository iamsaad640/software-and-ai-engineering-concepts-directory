# Rate limiting and admission control

[Directory](../README.md) · [Alphabetical index](../glossary.md)

## Concepts

- Fixed-window counter; boundary bursts
- Sliding-window log
- Sliding-window counter; weighted-window approximation
- Token bucket; burst capacity; refill rate
- Leaky bucket; GCRA
- Per-IP limits; per-user limits; per-tenant limits; hierarchical quotas
- Weighted requests; concurrency limits; admission control
- Distributed counters; Redis Lua; atomic updates; quota leasing
- Clock skew; TTL; hot keys; fail-open; fail-closed
- HTTP 429; Retry-After; load shedding; adaptive concurrency

## Reference starting points

These are category resources, not evidence that every term is defined by a single source.

- [Redis rate limiter pattern](https://redis.io/docs/latest/commands/incr/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web)
