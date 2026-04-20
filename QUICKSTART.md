# Thunder Tools - Quick Start Guide

Thunder development tools with **CLI** and **MCP (VS Code)** interfaces.

## What's Available

| Tool | Description | CLI | MCP |
|------|-------------|-----|-----|
| **Generate Plugin** | Create Thunder plugin skeleton | ✅ | ✅ |
| **Review Plugin** | Check code against framework rules | ✅ | ✅ |

## Quick Start - CLI

### 1. Generate a Plugin

```bash
cd /path/to/Thunder_MCP

python ThunderTools/core/thunder.py generate \
    --plugin-name NetworkManager \
    --output ThunderNanoServices
```

Output:
```
✅ Success! Plugin generated: ThunderNanoServices/NetworkManager
Generated 7 files:
  - NetworkManager.cpp
  - NetworkManager.h
  - CMakeLists.txt
  ...
```

### 2. Review the Plugin

```bash
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/NetworkManager
```

Output:
```
================================================================================
THUNDER PLUGIN REVIEW
================================================================================

Files reviewed: 4
Files with issues: 1
Total findings: 2

🔴 CRITICAL: 1
🟡 MEDIUM: 1
...
```

## Quick Start - MCP (VS Code)

### 1. Setup (One-time)

See [ThunderTools/MCP_SETUP.md](ThunderTools/MCP_SETUP.md) for full setup.

### 2. Use in VS Code

```
User: Generate a Thunder plugin named AudioControl

Copilot: [Shows interactive form]
         [User fills in details]
         ✅ Plugin generated at ThunderNanoServices/AudioControl

User: Review the AudioControl plugin

Copilot: [Shows review results]
         Files reviewed: 4
         Critical issues: 0
         ...
```

## CLI Help

```bash
# General help
python ThunderTools/core/thunder.py --help

# Generate help
python ThunderTools/core/thunder.py generate --help

# Review help
python ThunderTools/core/thunder.py review --help
```

## Examples

### Generate OOP Plugin with Interface

```bash
python ThunderTools/core/thunder.py generate \
    --plugin-name BluetoothControl \
    --mode oop \
    --interface ThunderInterfaces/interfaces/IBluetooth.h \
    --output ThunderNanoServices \
    --preconditions PLATFORM
```

### Review with JSON Output

```bash
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/MyPlugin \
    --format json > review_report.json
```

### Review Critical Issues Only

```bash
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/MyPlugin \
    --severity critical
```

## Complete Workflow

```bash
# Step 1: Generate plugin
python ThunderTools/core/thunder.py generate \
    --plugin-name MyPlugin \
    --output ThunderNanoServices

# Step 2: Review generated code
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin

# Step 3: Implement your logic
# (edit MyPlugin.cpp)

# Step 4: Review again
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/MyPlugin \
    --severity critical

# Step 5: Build and test
cd ThunderNanoServices/MyPlugin
# ... build steps ...
```

## Documentation

| Document | Description |
|----------|-------------|
| [ThunderTools/CLI_USAGE.md](ThunderTools/CLI_USAGE.md) | Complete CLI documentation |
| [ThunderTools/MCP_SETUP.md](ThunderTools/MCP_SETUP.md) | MCP server setup guide |
| [ThunderTools/ARCHITECTURE.md](ThunderTools/ARCHITECTURE.md) | Architecture overview |
| [ThunderTools/TOOLS_README.md](ThunderTools/TOOLS_README.md) | Tool descriptions |

## Architecture

```
Core Engines (ThunderTools/core/)
    ↓
CLI (python ThunderTools/core/thunder.py)    MCP (VS Code)
    ↓                          ↓
    └──────────┬───────────────┘
              User
```

Same core logic powers both CLI and MCP - consistency guaranteed!

## Troubleshooting

### "Module not found"

```bash
# Make sure you're in the workspace root
cd /path/to/Thunder_MCP
python ThunderTools/core/thunder.py --help
```

### "Interface file not found"

```bash
# Use absolute paths
python ThunderTools/core/thunder.py generate \
    --plugin-name MyPlugin \
    --interface "C:/full/path/to/interface.h"
```

## What's Next?

1. **Try it out** - Generate a test plugin
2. **Review code** - Check your existing plugins
3. **Read docs** - See [CLI_USAGE.md](ThunderTools/CLI_USAGE.md) for all options
4. **Setup MCP** - Use from VS Code (see [MCP_SETUP.md](ThunderTools/MCP_SETUP.md))

---

**Need help?** See full documentation in [ThunderTools/](ThunderTools/)

