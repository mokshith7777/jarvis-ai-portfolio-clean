"""Platform-neutral import smoke test for the installed JARVIS package."""

from __future__ import annotations

import sys

def main() -> int:
    try:
        import jarvis
        from jarvis.config import settings
        from jarvis.gateway import app
    except Exception as exc:
        print(f"JARVIS smoke test failed: {exc}")
        return 1

    if not getattr(jarvis, "__name__", "").startswith("jarvis"):
        print("JARVIS smoke test failed: package identity mismatch.")
        return 1
    if settings.port <= 0 or settings.port > 65535:
        print("JARVIS smoke test failed: invalid port.")
        return 1
    if not getattr(app, "routes", None):
        print("JARVIS smoke test failed: gateway has no routes.")
        return 1
    print(f"JARVIS smoke test passed on Python {sys.version.split()[0]}.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())