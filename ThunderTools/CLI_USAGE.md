# Thunder CLI - Command-Line Tools

Command-line interface for Thunder Framework development tools.

## Architecture

```
ThunderTools/
├── core/                      # Core Engines (Business Logic)
│   ├── review_engine.py       # Code review logic
│   └── skeleton_generator.py  # Plugin generation logic
│
├── cli/                       # CLI Interface
│   ├── thunder_cli.py         # Main CLI entry point
│   └── commands/
│       ├── generate.py        # Generate command
│       └── review.py          # Review command
│
├── tools/                     # MCP Tools (Server Interface)
│   ├── review_plugin.py       # Uses core.ReviewEngine
│   ├── review_directory.py    # Uses core.ReviewEngine
│   └── generate_skeleton.py   # Uses core.SkeletonGenerator
│
└── server.py                  # MCP Server
```

### Design Principles

1. **Core Engine** - All business logic lives in `core/`, completely independent
2. **CLI** - Thin wrapper around core, handles user input and formatting
3. **MCP Tools** - Thin wrapper around core, handles MCP protocol
4. **Reusability** - Same core engine used by both CLI and MCP

---

## Installation & Setup

### Quick Start

```bash
cd /path/to/Thunder_MCP

# Method 1: Use wrapper script (easiest)
python ThunderTools/core/thunder.py --help

# Method 2: Run as module
python -m ThunderTools.cli --help
```

### Optional: Add to PATH

**Windows (PowerShell):**
```powershell
# Add to current session
$env:PATH += ";C:\path\to\Thunder_MCP"

# Add permanently (edit PATH environment variable)
# Then you can run: python ThunderTools/core/thunder.py generate --plugin-name MyPlugin
```

**Linux/Mac:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/Thunder_MCP"
chmod +x ThunderTools/core/thunder.py

# Then you can run: python ThunderTools/core/thunder.py generate --plugin-name MyPlugin
```

---

## Commands

### 1. `generate` - Generate Plugin Skeleton

Generate a new Thunder plugin skeleton with all necessary files.

#### Basic Usage

```bash
# Minimal - generates in-process plugin
python ThunderTools/core/thunder.py generate --plugin-name MyPlugin

# Specify output directory
python ThunderTools/core/thunder.py generate \
    --plugin-name NetworkManager \
    --output ThunderNanoServices

# Out-of-process plugin with interface
python ThunderTools/core/thunder.py generate \
    --plugin-name BluetoothControl \
    --mode oop \
    --interface ThunderInterfaces/interfaces/IBluetooth.h \
    --output ThunderNanoServices
```

#### All Options

```bash
python ThunderTools/core/thunder.py generate \
    --plugin-name MyPlugin \
    --mode [in-process|oop|out-of-process] \
    --interface <path-to-interface.h> \  # Can specify multiple times
    --output <directory> \
    --config \                            # Generate config support (default)
    --no-config \                         # Skip config support
    --preconditions PLATFORM,NETWORK \
    --terminations PLATFORM \
    --controls TIME,NETWORK \
    --quiet
```

#### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--plugin-name`, `-n` | Plugin name (required) | - |
| `--mode`, `-m` | `in-process`, `oop`, or `out-of-process` | `in-process` |
| `--interface`, `-i` | Path to interface header (can use multiple times) | None |
| `--output`, `-o` | Output directory | `.` (current dir) |
| `--config` | Generate custom configuration support | True |
| `--no-config` | Skip custom configuration | - |
| `--preconditions` | Comma-separated subsystems (e.g., `PLATFORM,NETWORK`) | None |
| `--terminations` | Comma-separated termination subsystems | None |
| `--controls` | Comma-separated controlled subsystems | None |
| `--quiet`, `-q` | Suppress output messages | False |

#### Examples

**Example 1: Simple In-Process Plugin**
```bash
python ThunderTools/core/thunder.py generate \
    --plugin-name SimplePlugin \
    --output ThunderNanoServices \
    --no-config
```

**Example 2: OOP Plugin with Subsystems**
```bash
python ThunderTools/core/thunder.py generate \
    --plugin-name NetworkControl \
    --mode oop \
    --interface ThunderInterfaces/interfaces/INetworkControl.h \
    --output ThunderNanoServices \
    --preconditions PLATFORM \
    --controls NETWORK
```

**Example 3: Multiple Interfaces**
```bash
python ThunderTools/core/thunder.py generate \
    --plugin-name MultiFunctionPlugin \
    --interface ThunderInterfaces/interfaces/IInterface1.h \
    --interface ThunderInterfaces/interfaces/IInterface2.h \
    --output ThunderNanoServices
```

---

### 2. `review` - Review Plugin Code

Review C++ plugin files against Thunder framework guidelines.

#### Basic Usage

```bash
# Review single file
python ThunderTools/core/thunder.py review --file ThunderNanoServices/MyPlugin/MyPlugin.cpp

# Review entire directory
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin

# Review with custom output format
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/MyPlugin \
    --format markdown \
    --severity critical
```

#### All Options

```bash
python ThunderTools/core/thunder.py review \
    [--file <file.cpp> | --directory <dir>] \
    --recursive | --no-recursive \
    --format [text|json|markdown] \
    --severity [critical|high|medium|low|all] \
    --quiet
```

#### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--file`, `-f` | File to review (can use multiple times) | - |
| `--directory`, `-d` | Directory to review (mutually exclusive with `--file`) | - |
| `--recursive`, `-r` | Recursively review subdirectories | True |
| `--no-recursive` | Do not recurse into subdirectories | - |
| `--format` | Output format: `text`, `json`, or `markdown` | `text` |
| `--severity` | Minimum severity: `critical`, `high`, `medium`, `low`, `all` | `all` |
| `--quiet`, `-q` | Suppress output messages | False |

#### Output Formats

**Text (Default)**
```bash
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin
```

**JSON (Machine-Readable)**
```bash
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin --format json > report.json
```

**Markdown (Documentation)**
```bash
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin --format markdown > REVIEW.md
```

#### Exit Codes

- `0` - No critical issues found
- `1` - Critical issues found

#### Examples

**Example 1: Quick Review**
```bash
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/MyPlugin
```

**Example 2: Critical Issues Only**
```bash
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/MyPlugin \
    --severity critical
```

**Example 3: Multiple Files**
```bash
python ThunderTools/core/thunder.py review \
    --file MyPlugin.cpp \
    --file MyPlugin.h \
    --file Module.cpp
```

**Example 4: Generate JSON Report**
```bash
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices \
    --format json \
    --quiet > review_report.json
```

---

## Complete Workflow Example

Here's a complete workflow for creating and reviewing a new plugin:

```bash
# Step 1: Generate plugin skeleton
python ThunderTools/core/thunder.py generate \
    --plugin-name AudioControl \
    --mode oop \
    --interface ThunderInterfaces/interfaces/IAudioControl.h \
    --output ThunderNanoServices \
    --preconditions PLATFORM \
    --controls "TIME,NETWORK"

# Output:
# ✅ Success! Plugin generated: ThunderNanoServices/AudioControl
# Generated 7 files:
#   - AudioControl.cpp
#   - AudioControl.h
#   - CMakeLists.txt
#   - ...

# Step 2: Review generated code
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/AudioControl

# Output:
# THUNDER PLUGIN REVIEW
# Files reviewed: 4
# Files with issues: 1
# ...

# Step 3: Fix issues, then review again
# (edit code...)
python ThunderTools/core/thunder.py review --directory ThunderNanoServices/AudioControl --severity critical

# Step 4: Generate documentation report
python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/AudioControl \
    --format markdown > ThunderNanoServices/AudioControl/REVIEW.md
```

---

## Integration with MCP Server

The same core engines power both CLI and MCP tools:

**CLI:**
```bash
python ThunderTools/core/thunder.py generate --plugin-name MyPlugin
```

**MCP (via VS Code Copilot):**
```
@workspace generate a Thunder plugin named MyPlugin
```

Both use the same `SkeletonGenerator` from `core/`.

---

## Troubleshooting

### Command not found

**Issue:** `ThunderTools/core/thunder.py: command not found`

**Solution:**
```bash
# Use full path or run as module
python /full/path/to/Thunder_MCP/ThunderTools/core/thunder.py generate --plugin-name MyPlugin

# Or run as module
python -m ThunderTools.cli generate --plugin-name MyPlugin
```

### Import errors

**Issue:** `ModuleNotFoundError: No module named 'ThunderTools'`

**Solution:**
```bash
# Run from the workspace root (Thunder_MCP/)
cd /path/to/Thunder_MCP
python ThunderTools/core/thunder.py --help
```

### Plugin generation fails

**Issue:** `Interface files not found`

**Solution:**
```bash
# Use absolute paths for interfaces
python ThunderTools/core/thunder.py generate \
    --plugin-name MyPlugin \
    --interface "C:/full/path/to/ThunderInterfaces/interfaces/IMyPlugin.h"
```

---

## Advanced Usage

### Scripting Examples

**Batch Generate Multiple Plugins:**
```bash
#!/bin/bash
PLUGINS=("PluginA" "PluginB" "PluginC")

for plugin in "${PLUGINS[@]}"; do
    python ThunderTools/core/thunder.py generate \
        --plugin-name "$plugin" \
        --output ThunderNanoServices \
        --quiet
    echo "Generated $plugin"
done
```

**CI/CD Review Check:**
```bash
#!/bin/bash
# Fail build if critical issues found

python ThunderTools/core/thunder.py review \
    --directory ThunderNanoServices/MyPlugin \
    --severity critical \
    --format json > review.json

# Exit code 1 if critical issues found
if [ $? -ne 0 ]; then
    echo "❌ Critical issues found!"
    cat review.json
    exit 1
fi
```

---

## Help & Support

### Get Help

```bash
# General help
python ThunderTools/core/thunder.py --help

# Command-specific help
python ThunderTools/core/thunder.py generate --help
python ThunderTools/core/thunder.py review --help
```

### Common Subsystems

For `--preconditions`, `--terminations`, `--controls`:

- `PLATFORM` - Platform initialization
- `NETWORK` - Network connectivity
- `SECURITY` - Security/cryptography
- `TIME` - Time synchronization
- `GRAPHICS` - Graphics/display
- `BLUETOOTH` - Bluetooth functionality
- And more...

---

## Development

### Adding New Commands

1. Create command module: `ThunderTools/cli/commands/mycommand.py`
2. Add parser in `thunder_cli.py`
3. Implement `run_mycommand(args)` function
4. Use core engines from `ThunderTools.core`

### Running Tests

```bash
# Test generation
python ThunderTools/core/thunder.py generate --plugin-name TestPlugin --output /tmp

# Test review
python ThunderTools/core/thunder.py review --directory /tmp/TestPlugin
```

