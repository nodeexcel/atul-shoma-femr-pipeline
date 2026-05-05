---
name: Rootless Docker — no user directive in compose files
description: Server runs rootless Docker; never add user: directive to docker-compose services
type: feedback
originSessionId: 03ce2e1b-d66e-4c61-9283-53647745d1bc
---
Never add `user: "${UID}:${GID}"` or any `user:` directive to docker-compose service definitions for this project.

**Why:** The server runs rootless Docker, which automatically remaps container UIDs to the host user. Specifying `user:` explicitly causes permission errors on bind mounts and named volumes.

**How to apply:** When writing or editing any docker-compose.yml or docker-compose.prod.yml for this project, omit the `user:` field entirely from all services.
