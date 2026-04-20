#!/usr/bin/env python3
"""
Thunder CLI wrapper located under ThunderTools/core.

Usage:
    python ThunderTools/core/thunder.py generate --plugin-name MyPlugin
    python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin
"""

import sys
from pathlib import Path


# Ensure workspace root is on sys.path so `import ThunderTools` works
# even when this script is launched from outside the repository directory.
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from ThunderTools.cli import main


if __name__ == '__main__':
    sys.exit(main())
