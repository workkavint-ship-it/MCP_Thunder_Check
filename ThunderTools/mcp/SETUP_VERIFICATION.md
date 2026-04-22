# VS Code MCP Setup Verification

Follow these steps to verify your Thunder Tools MCP setup in VS Code.

---

## ✅ Step 1: Verify Configuration

Check `.vscode/settings.json` contains:

```json
{
  "github.copilot.chat.mcp.servers": {
    "thunder-tools": {
      "command": "python",
      "args": ["${workspaceFolder}/ThunderTools/mcp/server.py"]
    }
  }
}
```

**✓ Your config is correct!**

---

## ✅ Step 2: Test Server Manually

Run this command in your terminal:

```powershell
python ThunderTools/mcp/server.py
```

**Expected output:**
```
Loaded 13 rule categories
Loaded 13 rule categories
Thunder Tools MCP Server started
```

Press `Ctrl+C` to stop.

**✓ Server starts correctly!**

---

## ✅ Step 3: Verify Tool Names

Run this to see what tools are available:

```powershell
python -c "from ThunderTools.mcp.server import ThunderToolsServer; s = ThunderToolsServer(); tools = s.handle_list_tools(); print('\n'.join(t['name'] for t in tools['tools']))"
```

**Expected output:**
```
review_plugin
review_plugin_directory
generate_skeleton
```

**✓ Tools are registered correctly!**

---

## 🔴 Step 4: CRITICAL - Use Agent Mode

**This is the #1 reason MCP tools don't work in VS Code!**

1. Open Copilot Chat panel
2. Look at the top of the chat
3. Click the **mode dropdown**
4. Select **"Agent"** (NOT "Ask" or "Edit")

**MCP tools ONLY work in Agent mode!**

---

## ✅ Step 5: Restart VS Code

After any configuration change, you MUST restart VS Code:

**Option A: Full Restart**
- Close VS Code completely
- Reopen it

**Option B: Reload Window (faster)**
- Press `Ctrl+Shift+P`
- Type "Developer: Reload Window"
- Press Enter

**Do this now before testing!**

---

## ✅ Step 6: Test in Agent Mode

Open Copilot Chat in **Agent mode** and try:

### Test 1: Type # to see tools
```
#
```

You should see a dropdown with:
- `review_plugin`
- `review_plugin_directory`
- `generate_skeleton`

### Test 2: Direct tool call
```
#review_plugin_directory Dictionary1
```

### Test 3: Natural language
```
Review the Dictionary1 plugin for compliance issues
```

---

## 🐛 Troubleshooting

### Issue: Tools don't appear when typing `#`

**Causes:**
1. ❌ Not in Agent mode → Switch to Agent mode
2. ❌ VS Code not restarted → Restart VS Code
3. ❌ GitHub Copilot extension disabled → Enable it
4. ❌ Not logged into Copilot → Sign in

### Issue: `#review_plugin_directory` not recognized

**Causes:**
1. ❌ Typo in tool name → Use exact name: `review_plugin_directory`
2. ❌ Not in Agent mode → Switch to Agent mode
3. ❌ Server not loaded → Check Output panel for errors

### Issue: "ModuleNotFoundError"

**Solution:**
```powershell
pip install pyyaml
```

### Issue: Server not starting

**Check Python:**
```powershell
python --version  # Should be 3.8+
```

**Check imports:**
```powershell
python -c "from ThunderTools.core import ReviewEngine; print('OK')"
```

---

## 📊 Check VS Code Output Panel

1. Open Output panel: `View` → `Output`
2. Select **"GitHub Copilot"** from dropdown
3. Look for MCP-related messages
4. Check for error messages

---

## ✅ Working Example

After completing all steps above, this should work in Agent mode:

```
#review_plugin_directory Dictionary1
```

**Expected:** Copilot should call the `review_plugin_directory` tool and show you a comprehensive review report with:
- File structure analysis
- Compliance findings (critical/medium/low severity)
- Fix suggestions
- File-by-file details

---

## 🎯 Quick Checklist

Before asking "why doesn't it work?", verify:

- [ ] `.vscode/settings.json` has correct MCP config
- [ ] Server starts manually: `python ThunderTools/mcp/server.py`
- [ ] PyYAML installed: `pip install pyyaml`
- [ ] **Copilot Chat in Agent mode** (most common issue!)
- [ ] VS Code restarted after config changes
- [ ] GitHub Copilot extension enabled and logged in
- [ ] Python 3.8+ installed

---

## 💡 Pro Tips

**Discover tools:** Just type `#` in Agent mode to see all available tools

**Natural language works too:** You don't need to remember exact tool names. Just say "Review Dictionary1" and Copilot will call the right tool.

**Check tool arguments:** When you type `#review_plugin_directory`, VS Code may show you the expected arguments in the autocomplete.

---

## 🆘 Still Not Working?

1. **Run the verification script:**
   ```powershell
   python ThunderTools/mcp/setup_mcp.py
   ```

2. **Check exact error:** Look in VS Code Output → GitHub Copilot

3. **Test with natural language:** Instead of `#review_plugin_directory`, try:
   ```
   Review the Dictionary1 plugin for Thunder compliance issues
   ```

4. **Verify Agent mode:** This is critical - tools are invisible in Ask/Edit modes!

---

## ✅ Your Configuration Status

Based on the test output:

- ✅ Server configuration: **CORRECT**
- ✅ Server starts: **WORKING**  
- ✅ Tools registered: **3 tools available**
- ✅ Tool names: **Correct (review_plugin, review_plugin_directory, generate_skeleton)**

**Next step:** Make sure you're in **Agent mode** when testing!
