"""Small platform-neutral smoke test for the installed JARVIS package."""

from __future__ import annotations

import subprocess
import sys

def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "jarvis", "--help"],
        text=True,
        capture_output=True,
        timeout=30,
    )
    output = (result.stdout + result.stderr).lower()
    if result.returncode != 0:
        print(output)
        return result.returncode
    if "jarvis" not in output:
        print(output)
        print("JARVIS smoke test failed: branding not found.")
        return 1
    print("JARVIS smoke test passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())