# VSCode Setup Guide for AeroSpace-Alley-Comps

Complete guide to connect VSCode to this repository and set up your development environment.

---

## Method 1: Clone Directly in VSCode (Easiest)

### Step 1: Open VSCode

### Step 2: Open Command Palette
- **Windows/Linux:** `Ctrl + Shift + P`
- **macOS:** `Cmd + Shift + P`

### Step 3: Clone Repository
1. Type: `Git: Clone`
2. Select: **Clone from GitHub**
3. If prompted, sign in to GitHub
4. Paste repository URL: `https://github.com/yamas-sst/AeroSpace-Alley-Comps.git`
5. Choose a local folder to save the project
6. Click **"Open"** when prompted

### Step 4: Checkout the Working Branch
1. Open Command Palette again (`Ctrl/Cmd + Shift + P`)
2. Type: `Git: Checkout to...`
3. Select: `claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`

**Done!** Your VSCode is now connected to the repository.

---

## Method 2: Clone via Terminal, Then Open in VSCode

### Step 1: Open Terminal/Command Prompt

### Step 2: Navigate to Desired Location
```bash
cd ~/Documents  # or wherever you want the project
```

### Step 3: Clone Repository
```bash
git clone https://github.com/yamas-sst/AeroSpace-Alley-Comps.git
```

### Step 4: Enter Project Directory
```bash
cd AeroSpace-Alley-Comps
```

### Step 5: Checkout Working Branch
```bash
git checkout claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8
```

### Step 6: Open in VSCode
```bash
code .
```

If `code` command doesn't work:
- Open VSCode manually
- Go to **File → Open Folder**
- Navigate to and select `AeroSpace-Alley-Comps` folder

---

## Method 3: Already Have Repository? Just Open It

### If You Already Cloned It:
1. Open VSCode
2. **File → Open Folder** (or `Ctrl/Cmd + O`)
3. Navigate to your `AeroSpace-Alley-Comps` folder
4. Click **"Open"**

### Make Sure You're on the Right Branch:
1. Look at bottom-left corner of VSCode (shows current branch)
2. If not on `claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`:
   - Click the branch name
   - Select `claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`

---

## Python Environment Setup in VSCode

### Step 1: Install Python Extension
1. Click Extensions icon in left sidebar (or `Ctrl/Cmd + Shift + X`)
2. Search: **"Python"**
3. Install: **Python** by Microsoft (usually first result)

### Step 2: Create Virtual Environment
Open VSCode terminal (**Terminal → New Terminal** or `` Ctrl + ` ``):

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Select Python Interpreter
1. Open Command Palette (`Ctrl/Cmd + Shift + P`)
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python` (or `.\venv\Scripts\python.exe` on Windows)

### Step 4: Install Dependencies
In VSCode terminal (make sure venv is activated):
```bash
pip install -r resources/requirements.txt
```

You should see `(venv)` in your terminal prompt when virtual environment is active.

---

## Recommended VSCode Extensions

### Essential:
- **Python** (Microsoft) - Python language support
- **Pylance** (Microsoft) - Fast Python language server
- **GitLens** (GitKraken) - Enhanced Git capabilities

### Optional but Helpful:
- **Excel Viewer** (GrapeCity) - View .xlsx files in VSCode
- **Better Comments** - Colorful code comments
- **Python Indent** - Correct Python indentation
- **autoDocstring** - Generate Python docstrings

**Install Extensions:**
1. Click Extensions icon (left sidebar)
2. Search for extension name
3. Click **Install**

---

## Verify Everything Works

### 1. Check Python Environment
In VSCode terminal:
```bash
python --version
# Should show Python 3.7+

pip list
# Should show serpapi, requests, openpyxl, etc.
```

### 2. Check Git Branch
Bottom-left corner of VSCode should show:
```
claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8
```

### 3. Check File Structure
Your Explorer (left sidebar) should show:
```
AeroSpace-Alley-Comps/
├── AeroComps.py
├── resources/
├── data/
├── log/
├── LOCAL_SETUP_GUIDE.md
├── VSCODE_SETUP.md (this file)
└── ...
```

### 4. Test API Access
In VSCode terminal:
```bash
# Create config file first (see LOCAL_SETUP_GUIDE.md)
python quick_check.py
```

---

## Working with Git in VSCode

### View Changes
- **Source Control** icon in left sidebar (or `Ctrl/Cmd + Shift + G`)
- Shows modified, added, deleted files

### Commit Changes
1. Open Source Control panel
2. Stage changes (click **+** next to files)
3. Write commit message in text box
4. Click **✓ Commit** button

### Pull Latest Changes
1. Click **...** (three dots) in Source Control panel
2. Select **Pull**

Or use terminal:
```bash
git pull origin claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8
```

### Push Changes
1. Click **...** in Source Control panel
2. Select **Push**

Or use terminal:
```bash
git push origin claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8
```

### Switch Branches
- Click branch name in bottom-left corner
- Select different branch from list

---

## Create Configuration File in VSCode

### Step 1: Create File
1. Right-click on `resources/` folder in Explorer
2. Select **New File**
3. Name it: `config.json`

### Step 2: Paste Configuration
Copy this template (replace with your API key):

```json
{
  "api_keys": [
    {
      "label": "My-SerpAPI-Key",
      "key": "PASTE_YOUR_SERPAPI_KEY_HERE",
      "limit": 250,
      "priority": 1,
      "notes": "Get key from serpapi.com/manage-api-key"
    }
  ],
  "settings": {
    "testing_mode": true,
    "testing_company_limit": 1,
    "input_file": "data/Test_3_Companies.xlsx",
    "output_file": "output/Aerospace_Alley_SkilledTrades_Jobs.xlsx",
    "max_api_calls_per_key": 250,
    "min_interval_seconds": 1.2,
    "max_threads": 5
  }
}
```

### Step 3: Save
- `Ctrl/Cmd + S` or **File → Save**

**Important:** This file is in `.gitignore` so it won't be committed (keeps your API key private).

---

## Running Python Scripts in VSCode

### Method 1: Right-Click in Editor
1. Open `AeroComps.py` (or any Python file)
2. Right-click in editor
3. Select **"Run Python File in Terminal"**

### Method 2: Use Terminal
```bash
python AeroComps.py
```

### Method 3: Use Run Button
- Top-right corner of editor has a **▶ Run** button
- Click it to run current Python file

### Method 4: Keyboard Shortcut
- Open Python file
- Press `Ctrl/Cmd + F5` to run without debugging
- Or `F5` to run with debugging

---

## Debugging in VSCode

### Set Breakpoints
- Click in the gutter (left of line numbers)
- Red dot appears = breakpoint

### Start Debugging
1. Press `F5`
2. Select **"Python File"** if prompted
3. Script runs and stops at breakpoints

### Debug Controls (when paused)
- **Continue** (F5) - Run until next breakpoint
- **Step Over** (F10) - Execute current line
- **Step Into** (F11) - Enter function calls
- **Step Out** (Shift+F11) - Exit current function

### View Variables
- **Variables** panel shows all current variables
- Hover over variables in code to see values

---

## Useful VSCode Shortcuts

### General
- **Command Palette:** `Ctrl/Cmd + Shift + P`
- **Quick Open File:** `Ctrl/Cmd + P`
- **Toggle Terminal:** `` Ctrl/Cmd + ` ``
- **Save:** `Ctrl/Cmd + S`
- **Save All:** `Ctrl/Cmd + K, S`

### Editing
- **Find:** `Ctrl/Cmd + F`
- **Find in Files:** `Ctrl/Cmd + Shift + F`
- **Multi-cursor:** `Alt + Click` (Windows/Linux) or `Opt + Click` (macOS)
- **Duplicate Line:** `Shift + Alt + Down/Up`
- **Comment Line:** `Ctrl/Cmd + /`

### Python Specific
- **Run File:** `Ctrl/Cmd + F5`
- **Debug File:** `F5`
- **Select Interpreter:** `Ctrl/Cmd + Shift + P` → "Python: Select Interpreter"

### Git
- **Source Control:** `Ctrl/Cmd + Shift + G`
- **View Changes:** Click file in Source Control panel

---

## Troubleshooting

### Issue: "code" Command Not Found

**On macOS:**
1. Open VSCode
2. `Cmd + Shift + P`
3. Type: "Shell Command: Install 'code' command in PATH"
4. Restart terminal

**On Windows:**
- VSCode usually adds to PATH during installation
- Reinstall VSCode with "Add to PATH" option checked

**On Linux:**
```bash
# Add this to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/usr/share/code/bin"
```

### Issue: Python Extension Not Finding Interpreter

**Fix:**
1. `Ctrl/Cmd + Shift + P`
2. "Python: Select Interpreter"
3. If your venv isn't listed, click "Enter interpreter path..."
4. Browse to: `./venv/bin/python` (or `.\venv\Scripts\python.exe` on Windows)

### Issue: Imports Showing as Errors

**Fix:**
1. Make sure virtual environment is activated
2. Make sure you selected the venv Python interpreter
3. Restart VSCode: `Ctrl/Cmd + Shift + P` → "Developer: Reload Window"

### Issue: Terminal Not Using Virtual Environment

**Fix:**
1. Close all terminals in VSCode
2. Open new terminal (`` Ctrl/Cmd + ` ``)
3. Should auto-activate venv (see `(venv)` in prompt)
4. If not, manually activate:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

### Issue: Git Not Working in VSCode

**Fix:**
1. Make sure Git is installed: `git --version` in terminal
2. If not installed:
   - Windows: [git-scm.com](https://git-scm.com)
   - macOS: `xcode-select --install`
   - Linux: `sudo apt install git` or `sudo yum install git`
3. Restart VSCode

---

## VSCode Settings for Python (Optional)

Create `.vscode/settings.json` in project root:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  },
  "files.watcherExclude": {
    "**/venv/**": true
  }
}
```

This configures:
- Default Python interpreter
- Auto-formatting on save
- Linting (error checking)
- Hide Python cache files

---

## Quick Start Checklist

After connecting VSCode to the repository:

- [ ] Python extension installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r resources/requirements.txt`)
- [ ] Correct branch checked out (`claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`)
- [ ] Python interpreter selected (venv)
- [ ] `resources/config.json` created with API key
- [ ] Ran `python setup_check.py` (all green checks)
- [ ] Ran `python quick_check.py` (API accessible)

**Now you're ready to run:**
```bash
python AeroComps.py
```

---

## Next Steps

1. **Follow LOCAL_SETUP_GUIDE.md** for detailed project setup
2. **Run Test 1** (1 company) to validate everything works
3. **Check output/** folder for results Excel file
4. **Review log/api_audit.jsonl** to see protection system in action

---

## Getting Help

**VSCode Issues:**
- Official Docs: [code.visualstudio.com/docs](https://code.visualstudio.com/docs)
- Python in VSCode: [code.visualstudio.com/docs/python](https://code.visualstudio.com/docs/python/python-tutorial)

**Project Issues:**
- See LOCAL_SETUP_GUIDE.md
- See QUICKSTART.md
- See SESSION_HANDOFF.md

**Git Issues:**
- Git Basics: [git-scm.com/book](https://git-scm.com/book/en/v2)
- GitHub Docs: [docs.github.com](https://docs.github.com)

---

## Summary

**Fastest way to get started:**

```bash
# 1. Clone
git clone https://github.com/yamas-sst/AeroSpace-Alley-Comps.git
cd AeroSpace-Alley-Comps

# 2. Open in VSCode
code .

# 3. In VSCode terminal:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r resources/requirements.txt

# 4. Create resources/config.json with your API key

# 5. Test
python quick_check.py
python AeroComps.py
```

**You're ready to code! 🚀**
