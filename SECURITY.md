# Security model

JARVIS treats model output as untrusted input. Smart approval is the default. Catastrophic operations are blocked regardless of approval mode, secrets are kept out of prompt memory, and the container defaults to non-root with dropped capabilities.

The first implementation's Python executor is a foundation, not a complete host security boundary. Production deployments should move programmatic execution into a separate hardened sandbox with restricted mounts, credentials and egress. Never treat the model as a security authority.
