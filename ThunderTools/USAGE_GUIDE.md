# Thunder Tools - Usage Guide

## 🎯 How to Use the Tools Conversationally

The Thunder MCP tools are designed to work **interactively through chat**. The AI assistant will ask you questions to gather all the information needed, then generate or review your plugin.

---

## 🏗️ Generating a Plugin (Interactive Workflow)

### Step-by-Step Example

**You:** Generate a Thunder plugin

**AI:** I'll help you generate a Thunder plugin! Let me gather the details:

1. **What should the plugin be called?**

**You:** MediaController

**AI:** Great! Now:

2. **Should it run as an out-of-process (OOP) plugin?**
   - `true` = Out-of-process (separate process)
   - `false` = In-process (runs in Thunder framework)

**You:** Yes, make it out-of-process

**AI:** 

3. **Do you have any interface files to implement?**
   Provide full paths like: `/path/to/ThunderInterfaces/interfaces/IMediaControl.h`
   Or say "none" for a basic skeleton.

**You:** None for now

**AI:**

4. **Does your plugin need any Thunder subsystems?**
   
   - **Preconditions** (required before activation): PLATFORM, NETWORK, etc.
   - **Terminations** (triggers deactivation): NETWORK, etc.
   - **Controls** (subsystems this plugin manages): TIME, NETWORK, etc.

**You:** Needs PLATFORM as precondition, controls TIME

**AI:** Perfect! Let me generate the plugin...

[Calls `generate_skeleton` tool with all gathered info]

✅ **Plugin generated at:** `MediaController/`

---

## 🔍 Reviewing a Plugin

### Quick Review Examples

**Simple:**
```
Review ThunderNanoServices/NetworkControl
```

**Specific Files:**
```
Check BluetoothAudio.cpp for compliance issues
Review this file
```

**After Generation:**
```
Generate MediaController plugin, then review it
```

---

## 💬 Full Conversation Example

**You:** I want to create a new Thunder plugin

**AI:** I'll help you create a Thunder plugin! First, what would you like to call it?

**You:** Let's call it AudioService

**AI:** Great! Should AudioService run as an out-of-process (OOP) plugin, or in-process?

**You:** In-process

**AI:** Perfect. Do you have any existing interface header files you want to implement? For example, paths like:
- `/path/to/ThunderInterfaces/interfaces/IAudio.h`

Or I can create a basic skeleton without specific interfaces.

**You:** No interfaces yet, just create a basic one

**AI:** Understood! Does your plugin need any Thunder subsystems?

- **Preconditions**: Subsystems required before activation (like PLATFORM, NETWORK)
- **Terminations**: Subsystems that trigger deactivation
- **Controls**: Subsystems your plugin manages

**You:** It needs NETWORK as a precondition

**AI:** Perfect! Let me generate the AudioService plugin...

[Generates plugin]

✅ **Plugin Created!**

**Location:** `AudioService/`
**Mode:** In-Process
**Preconditions:** NETWORK

**Next steps:**
1. Review the generated code
2. Implement your plugin logic in AudioService.cpp
3. Update CMakeLists.txt as needed

Would you like me to review the generated plugin for compliance issues?

**You:** Yes, review it

[Reviews plugin and shows findings]

---

## 🎨 Customization Options

### When asking for plugin generation, you can specify:

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Plugin Name** | Name of your plugin | `MediaController`, `AudioService` |
| **OOP Mode** | Out-of-process or in-process | `true` / `false`, `OOP` / `in-process` |
| **Interface Paths** | Header files to implement | Full paths to `.h` files in ThunderInterfaces |
| **Preconditions** | Required subsystems | `PLATFORM`, `NETWORK` |
| **Terminations** | Deactivation triggers | `NETWORK`, `PLATFORM` |
| **Controls** | Managed subsystems | `TIME`, `NETWORK` |

### Common subsystems:
- `PLATFORM` - Platform initialization
- `NETWORK` - Network connectivity
- `GRAPHICS` - Graphics subsystem
- `SECURITY` - Security subsystem
- `TIME` - Time/clock management

---

## 🚀 Advanced Workflows

### Generate and Review
```
Generate a plugin called NetworkMonitor with NETWORK precondition, then review it for issues
```

### Review Multiple Plugins
```
Review all plugins in ThunderNanoServices
```

### Generate with Interface
```
Generate a plugin called TestService using interface /full/path/to/ThunderInterfaces/interfaces/ITest.h
```

---

## ⚡ Quick Commands

| What you want | Just say |
|---------------|----------|
| Create plugin | `Generate a plugin called [Name]` |
| Review plugin | `Review ThunderNanoServices/[PluginName]` |
| Check file | `Check this file for compliance` |
| Combined | `Create [Name] and review it` |

---

## 💡 Tips

1. **Be conversational** - The AI will ask for what it needs
2. **Provide details gradually** - No need to give everything upfront
3. **Review after generation** - Always check generated code for compliance
4. **Iteration is easy** - Generate, review, fix, repeat
5. **Ask questions** - The AI knows the Thunder framework guidelines

---

## 🆘 Common Questions

**Q: Do I need to know all parameters upfront?**
A: No! Just say "generate a plugin" and the AI will ask you questions.

**Q: What if I don't have interface files?**
A: That's fine! The tool will create a basic skeleton with a minimal interface.

**Q: Can I generate plugins without VS Code?**
A: Yes! Works in Claude Desktop, Cursor, or any MCP-compatible client.

**Q: How do I know what subsystems to use?**
A: Ask the AI: "What subsystems are available?" or "What should I use for a network plugin?"

---

## 📖 See Also

- [MCP_SETUP.md](MCP_SETUP.md) - Setup instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [README.md](README.md) - Quick start guide
