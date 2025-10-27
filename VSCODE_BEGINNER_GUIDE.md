# VSCode Setup for Complete Beginners

This guide assumes you've NEVER used VSCode before. We'll go through everything step-by-step with pictures descriptions.

**Time needed:** 15-20 minutes

---

## Part 1: Install VSCode (5 minutes)

### Step 1: Download VSCode

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: **https://code.visualstudio.com**
3. You'll see a big blue button that says **"Download for [Your Operating System]"**
4. Click that button
5. Wait for the download to finish (it's about 90 MB)

### Step 2: Install VSCode

**On Windows:**
1. Find the downloaded file (usually in your Downloads folder)
2. Double-click the file (it's called something like `VSCodeSetup.exe`)
3. Click **"Yes"** if Windows asks permission
4. Click **"I accept the agreement"** → Click **"Next"**
5. Click **"Next"** again (default location is fine)
6. Click **"Next"** again (default name is fine)
7. **IMPORTANT:** Make sure these boxes are checked:
   - ✅ Add "Open with Code" action to Windows Explorer
   - ✅ Add to PATH (this is important!)
8. Click **"Next"** → Click **"Install"**
9. Wait for installation (about 1 minute)
10. Click **"Finish"**

**On macOS:**
1. Find the downloaded file (usually in Downloads folder)
2. Double-click the file (it's called `VSCode-darwin.zip`)
3. Drag the **Visual Studio Code** icon to your **Applications** folder
4. Double-click Visual Studio Code in Applications
5. If it says "from an unidentified developer", click **"Open"**

**On Linux:**
1. If you're using Linux, you probably know what to do! 😊
2. But just in case: Open the .deb or .rpm file and follow the installer

### Step 3: Open VSCode for the First Time

**Windows:**
- Click the Windows Start button
- Type: `code`
- Click **Visual Studio Code**

**macOS:**
- Press `Cmd + Space` (this opens Spotlight)
- Type: `code`
- Press Enter

**Or just look for the VSCode icon on your desktop or applications!**

You should see a welcome screen that says "Welcome" at the top. Great! VSCode is open.

---

## Part 2: Install Python (If You Don't Have It)

### Check If You Already Have Python

1. In VSCode, look at the top menu bar
2. Click **"Terminal"**
3. Click **"New Terminal"**
4. You'll see a black or white box appear at the bottom (this is the terminal)
5. Type this and press Enter:
   ```
   python --version
   ```
6. **If you see something like "Python 3.9.7"** → You have Python! Skip to Part 3.
7. **If you see "command not found" or an error** → Continue below to install Python.

### Install Python (If Needed)

**Windows:**
1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow button: **"Download Python 3.x.x"**
3. Run the downloaded file
4. **⚠️ IMPORTANT:** Check the box that says **"Add Python to PATH"** (at the bottom)
5. Click **"Install Now"**
6. Wait for installation
7. Click **"Close"**
8. **Close VSCode completely** (so it can see the new Python)
9. Open VSCode again

**macOS:**
1. Open Terminal (press `Cmd + Space`, type `terminal`, press Enter)
2. Copy and paste this entire line, then press Enter:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Wait for it to finish (it might ask for your password)
4. Then type this and press Enter:
   ```
   brew install python3
   ```
5. Wait for installation (5-10 minutes)

---

## Part 3: Get the Project Code (10 minutes)

Now we'll download the project code from GitHub to your computer.

### Step 1: Open the Command Palette

This is VSCode's search box for commands.

1. Look at the top of your VSCode window
2. Do one of these (depending on your computer):
   - **Windows:** Press `Ctrl + Shift + P` (all three keys together)
   - **Mac:** Press `Cmd + Shift + P` (all three keys together)
3. You should see a text box appear at the top that says **"Show and Run Commands"**

**If nothing happened:** Try clicking on the VSCode window first to make sure it's active, then try again.

### Step 2: Clone the Repository (Download the Code)

Think of "clone" as "download a copy of the project".

1. In that command box at the top, type: `clone`
2. You'll see a list of options appear below
3. Look for one that says **"Git: Clone"** (it has a little branch icon)
4. Click on **"Git: Clone"**

### Step 3: Sign Into GitHub (If Asked)

VSCode might ask you to sign in to GitHub.

1. If you see a button that says **"Allow"** or **"Sign in to GitHub"**, click it
2. Your web browser will open
3. If you're not logged into GitHub, log in with your username and password
4. Click **"Authorize Visual-Studio-Code"** or **"Continue"**
5. You might see a message "Visual Studio Code wants to open" → Click **"Open"**
6. Go back to VSCode (it should be ready now)

**Don't have a GitHub account?**
- You can skip signing in
- Just paste the repository URL in the next step

### Step 4: Enter the Project URL

1. You should see a text box that says **"Provide repository URL"**
2. Click in that box
3. Copy this ENTIRE line (highlight it, then Ctrl+C or Cmd+C):
   ```
   https://github.com/yamas-sst/AeroSpace-Alley-Comps.git
   ```
4. Paste it into VSCode (Ctrl+V or Cmd+V)
5. Press **Enter**

### Step 5: Choose Where to Save It

VSCode will ask "where do you want to save this project?"

1. A file browser window will open
2. Navigate to where you want the project (I recommend **Documents** folder)
3. Click **"Select Repository Location"** or **"Choose"**

Now VSCode will download the project. You'll see a progress message at the bottom right. Wait for it to finish (30 seconds to 2 minutes depending on your internet).

### Step 6: Open the Project

1. When it's done, you'll see a popup at the bottom right that says:
   **"Would you like to open the cloned repository?"**
2. Click **"Open"**

**If you accidentally closed that popup:**
1. Click **"File"** in the top menu
2. Click **"Open Folder"**
3. Navigate to where you saved it (probably Documents)
4. Find the folder called **"AeroSpace-Alley-Comps"**
5. Click it once to select it
6. Click **"Open"** or **"Select Folder"**

You should now see a list of files on the left side of VSCode! The folder tree should show files like:
- AeroComps.py
- LOCAL_SETUP_GUIDE.md
- resources (folder)
- data (folder)
- etc.

**Success!** You've got the code on your computer!

---

## Part 4: Switch to the Right Branch (2 minutes)

Think of a "branch" as a specific version of the project. We need the testing version.

### Step 1: Look at the Bottom Left Corner

1. Look at the very bottom left corner of VSCode
2. You should see a little icon that looks like this: ⎇ or a branch symbol
3. Next to it, you'll see some text (probably says "main" or "master")

### Step 2: Click on That Branch Name

1. Click on that text in the bottom left corner
2. A list will appear at the top of the screen

### Step 3: Select the Testing Branch

1. In that list, look for: **`claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`**
2. It might take a second to load the list
3. Scroll down if you don't see it right away
4. Click on **`claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`**

Now look at the bottom left corner again. It should now say **`claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8`**

**Perfect!** You're on the right version of the code.

---

## Part 5: Install Python Extension (2 minutes)

VSCode needs an extension to understand Python code.

### Step 1: Open the Extensions Panel

Look at the left side of VSCode. You'll see a vertical row of icons.

1. Find the icon that looks like 4 squares (with one square slightly separated)
   - It's usually the 5th or 6th icon from the top
   - If you hover over it, it says **"Extensions"**
2. Click on that icon

The left panel should now show **"EXTENSIONS"** at the top.

### Step 2: Search for Python

1. At the top of the extensions panel, there's a search box that says **"Search Extensions in Marketplace"**
2. Click in that box
3. Type: `python`
4. Press Enter

### Step 3: Install the Python Extension

You'll see a list of extensions. The first one should be:

**Python** by Microsoft
- It has a blue Python logo
- It says "IntelliSense (Pylance), Linting, Debugging..."

1. Click on that **"Python"** extension (the first one)
2. You'll see a blue button that says **"Install"**
3. Click **"Install"**
4. Wait for it to install (about 30 seconds)
5. The button will change to say **"Installed"** with a gear icon

**Done!** VSCode can now understand Python.

---

## Part 6: Open the Terminal (1 minute)

The terminal is where we type commands to run the code.

### Step 1: Open a New Terminal

1. Look at the top menu bar
2. Click **"Terminal"**
3. Click **"New Terminal"**

A panel will appear at the bottom of VSCode with a command line.

**What you'll see:**
- **Windows:** Looks like `C:\Users\YourName\Documents\AeroSpace-Alley-Comps>`
- **Mac/Linux:** Looks like `~/Documents/AeroSpace-Alley-Comps $`

This is the terminal. You can type commands here.

---

## Part 7: Set Up Python Environment (5 minutes)

We need to create a special isolated space for this project's Python packages.

### Step 1: Create a Virtual Environment

In the terminal at the bottom, type this EXACT command (copy and paste it):

**On Windows:**
```
python -m venv venv
```

**On Mac/Linux:**
```
python3 -m venv venv
```

Press **Enter**.

You won't see much happen. It might take 10-30 seconds. Wait until you see the command prompt again (the `>` or `$` symbol).

**What just happened?**
You created a folder called "venv" that will store all the project's Python packages.

### Step 2: Activate the Virtual Environment

Now we need to "turn on" that environment.

**On Windows:**
Type this and press Enter:
```
venv\Scripts\activate
```

**On Mac/Linux:**
Type this and press Enter:
```
source venv/bin/activate
```

**How do you know it worked?**
Look at your terminal. You should now see `(venv)` at the beginning of the line, like this:
- Windows: `(venv) C:\Users\...\AeroSpace-Alley-Comps>`
- Mac/Linux: `(venv) ~/Documents/AeroSpace-Alley-Comps $`

**If you see `(venv)`** → Success! ✅

**If you don't see `(venv)`:**
- Make sure you typed the command exactly right
- Try closing the terminal (click the trash can icon) and opening a new one
- Try the command again

### Step 3: Install the Required Packages

Now we'll install all the Python packages this project needs.

Copy this EXACT command and paste it in the terminal:
```
pip install -r resources/requirements.txt
```

Press **Enter**.

**What you'll see:**
- Lots of text scrolling by
- Lines like "Downloading...", "Installing...", "Successfully installed..."
- This takes 1-3 minutes
- Don't close VSCode while this is happening!

Wait until you see the prompt again with `(venv)` at the start.

**Success message:** You should see something like:
```
Successfully installed serpapi-2.4.2 requests-2.31.0 openpyxl-3.1.2 ...
```

**If you see an error about pip version:**
- Type: `python -m pip install --upgrade pip`
- Press Enter
- Then try the install command again

**Perfect!** All the required packages are now installed.

---

## Part 8: Tell VSCode Which Python to Use (2 minutes)

VSCode needs to know to use the Python in our virtual environment.

### Step 1: Open Command Palette Again

Remember this from before?

- **Windows:** Press `Ctrl + Shift + P`
- **Mac:** Press `Cmd + Shift + P`

### Step 2: Select Python Interpreter

1. In the command box that appears, type: `python select`
2. You'll see **"Python: Select Interpreter"** in the list
3. Click on it

### Step 3: Choose the venv Python

You'll see a list of Python installations. Look for one that says:

**`./venv/bin/python`** or **`.\venv\Scripts\python.exe`**

It might also show the version number like "Python 3.9.7"

1. Click on the one that has **venv** in the path
2. The list will close

**How do you know it worked?**
Look at the very bottom right corner of VSCode. You should see something like:
- `Python 3.9.7 64-bit ('venv': venv)`

**Great!** VSCode is now using the right Python.

---

## Part 9: Create Your Configuration File (5 minutes)

This file tells the program your SerpAPI key and settings.

### Step 1: Get Your SerpAPI Key

1. Open your web browser
2. Go to: **https://serpapi.com**
3. Click **"Sign Up"** or **"Sign In"** (top right)
4. Create an account (it's free - you get 100 searches per month)
5. After logging in, go to: **https://serpapi.com/manage-api-key**
6. You'll see your API key - it's a long string of letters and numbers
7. Click the **"Copy"** button next to it
8. **Keep this browser tab open** - you'll need to paste this key in a moment

### Step 2: Create the Config File

Back in VSCode:

1. Look at the left panel (it shows the file tree)
2. Find the **"resources"** folder
3. **Right-click** on the **"resources"** folder
4. Select **"New File"** from the menu
5. Type: `config.json`
6. Press **Enter**

A new empty file will open in the middle of VSCode.

### Step 3: Paste the Configuration Template

Copy this ENTIRE block (click anywhere in it, then Ctrl+A to select all, Ctrl+C to copy):

```json
{
  "api_keys": [
    {
      "label": "My-SerpAPI-Key",
      "key": "PASTE_YOUR_KEY_HERE",
      "limit": 250,
      "priority": 1,
      "notes": "My SerpAPI key from serpapi.com"
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

Now paste it into the empty config.json file in VSCode (Ctrl+V or Cmd+V).

### Step 4: Replace with Your Real API Key

1. Look for the line that says: `"key": "PASTE_YOUR_KEY_HERE",`
2. Click on the text `PASTE_YOUR_KEY_HERE` (between the quotes)
3. Select it all (double-click on it)
4. Paste your actual SerpAPI key that you copied earlier (Ctrl+V or Cmd+V)

**The line should now look like:**
```json
"key": "801d79de5fa4d16e67d77c3b0cf1d2090a394d0f52df23aebd5deecf9d653cc4",
```
(But with YOUR key, not this example)

### Step 5: Save the File

- Press `Ctrl + S` (Windows/Linux) or `Cmd + S` (Mac)
- Or click **"File"** → **"Save"**

**You'll know it saved when:**
- The file name `config.json` in the tab no longer has a white dot next to it
- The white dot means "unsaved changes"

**Perfect!** Your configuration is ready.

---

## Part 10: Verify Everything Is Set Up Correctly (2 minutes)

Let's check that everything is working before we run the actual program.

### Step 1: Make Sure Terminal Is Open

Look at the bottom of VSCode. If you don't see a terminal panel:

1. Click **"Terminal"** in the top menu
2. Click **"New Terminal"**

Make sure you see `(venv)` at the start of the line.

**If you don't see (venv):**
Run the activate command again:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### Step 2: Run the Setup Check

In the terminal, type this EXACT command:
```
python setup_check.py
```

Press **Enter**.

**What you should see:**
```
✅ Python Version: 3.x.x
✅ Dependencies Installed: All required packages found
✅ Directory Structure: All directories exist
✅ Configuration File: Valid JSON, API keys configured
✅ Input Data Files: Test and production files found
✅ Protection System: Rate limiter module loaded

🎉 Setup Complete! Ready to run.
```

**All green checkmarks? Perfect! ✅**

**If you see red X marks or errors:**
- Read the error message - it tells you what's wrong
- Common issues:
  - Missing packages → Run `pip install -r resources/requirements.txt` again
  - Config file error → Check that config.json is saved and has your API key
  - Python version too old → Make sure you have Python 3.7 or higher

---

## Part 11: Test API Access (1 minute)

Let's check if your computer can access the SerpAPI service.

### In the terminal, type:
```
python quick_check.py
```

Press **Enter**.

**Good Response (You'll see green checkmarks):**
```
✅ API is accessible (200 - Success)
   Status: Ready to run!
   Found: 10 sample jobs
```

**This means:** Your local internet connection can reach SerpAPI! You can run the program!

**Bad Response (You'll see red X):**
```
❌ Still blocked (403 - Access Denied)
   Status: IP block still active
   Suggestion: Try again in a few hours
```

**This means:** Your IP is also blocked. You might need to:
- Try from a different network (like mobile hotspot)
- Wait 24-48 hours for the block to clear
- Use a VPN

---

## Part 12: Run the Program! (2 minutes)

If your API test passed (green checkmark), you're ready to run!

### Step 1: Run Test 1 (1 Company)

This is the safest test - it only checks 1 company and uses just 3 API calls.

In the terminal, type:
```
python AeroComps.py
```

Press **Enter**.

### Step 2: Watch It Run

**You should see:**
```
======================================================================
AEROSPACE ALLEY JOB SCANNER - Configuration Loading
======================================================================
✅ Configuration loaded successfully from config.json
   API Keys found: 1
   - My-SerpAPI-Key: 801d79de5fa4d16e... (limit: 250)

🧪 TESTING MODE ENABLED: Will process only 1 company
======================================================================

🛡️ PROTECTION SYSTEM ACTIVATED
   Rate Limit: 60 calls/hour
   Circuit Breaker: 3 failure threshold
   Batch Processing: 10 companies per batch

Loading company list from: data/Test_3_Companies.xlsx
🧪 TESTING MODE: Processing 1 of 3 companies
   Companies to test: Barnes Aerospace East Granby

Processing companies: 100%|██████████| 1/1 [00:15<00:00, 15.23s/it]

[Barnes Aerospace East Granby] → 12 skilled-trade jobs found

============================================================
API Usage: 3/250 calls used (My-SerpAPI-Key)
============================================================

✅ Results saved to: output/Aerospace_Alley_SkilledTrades_Jobs.xlsx
```

**This takes about 15-20 seconds.**

Don't close VSCode while it's running! Wait until you see "Results saved to..." message.

### Step 3: Check Your Results

1. In the left file panel, look for the **"output"** folder
2. Click on it to expand it
3. You should see: **`Aerospace_Alley_SkilledTrades_Jobs.xlsx`**
4. **Right-click** on that file
5. Select **"Reveal in File Explorer"** (Windows) or **"Reveal in Finder"** (Mac)
6. Your file browser will open showing that Excel file
7. Double-click it to open it in Excel

**You should see a spreadsheet with job listings!**
- Company names
- Job titles
- Locations
- Job URLs
- Other details

**🎉 Congratulations! You just ran the program successfully!**

---

## Part 13: What to Do Next

### Run More Companies (Optional)

If Test 1 worked, you can test more companies:

1. Open the file **`resources/config.json`** (in the left file tree)
2. Find the line: `"testing_company_limit": 1,`
3. Change the `1` to `3`
4. Save the file (Ctrl+S or Cmd+S)
5. Run `python AeroComps.py` again

This will test 3 companies (~40 seconds, 9 API calls).

### Run All 137 Companies (Advanced)

**⚠️ WARNING:** This uses 411 API calls! Only do this if:
- Test 1 and Test 2 worked perfectly
- You have enough API credits (100 free per month, so you'd need a paid plan or 5 free accounts)

To run all companies:
1. Open **`resources/config.json`**
2. Change `"testing_mode": true,` to `"testing_mode": false,`
3. Save the file
4. Run `python AeroComps.py`
5. This takes 40-50 minutes

---

## Common Issues & Solutions

### "python: command not found" or "python3: command not found"

**Solution:**
- Make sure Python is installed (see Part 2)
- Try using `python3` instead of `python` in all commands
- On Windows, make sure you checked "Add Python to PATH" during installation

### "No module named 'serpapi'" or similar error

**Solution:**
- Make sure you see `(venv)` in your terminal
- If not, activate it:
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- Run: `pip install -r resources/requirements.txt`

### "FileNotFoundError: config.json"

**Solution:**
- Make sure you created `resources/config.json` (Part 9)
- Make sure you saved it (Ctrl+S or Cmd+S)
- Check that it's inside the `resources` folder, not somewhere else

### Terminal shows weird characters or doesn't work

**Solution:**
- Click the trash can icon in the terminal panel to close it
- Open a new terminal: **Terminal → New Terminal**
- Try your command again

### "403 Access Denied" when running quick_check.py

**This means:**
- Your IP address is blocked by SerpAPI
- This happened in the Claude Code environment too
- Try a different internet connection (mobile hotspot, different WiFi)
- Or wait 24-48 hours for the block to clear

### VSCode is frozen or not responding

**Solution:**
- Wait 30 seconds (it might just be thinking)
- If still frozen, close VSCode completely
- Open it again
- Open your project: **File → Open Folder** → Select `AeroSpace-Alley-Comps`

---

## Quick Reference: Commands You'll Use

Copy these for quick reference:

**Activate virtual environment:**
```bash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

**Check setup:**
```bash
python setup_check.py
```

**Test API access:**
```bash
python quick_check.py
```

**Run the program:**
```bash
python AeroComps.py
```

**Install packages (if needed):**
```bash
pip install -r resources/requirements.txt
```

---

## Keyboard Shortcuts to Remember

**Command Palette (opens command search):**
- Windows/Linux: `Ctrl + Shift + P`
- Mac: `Cmd + Shift + P`

**Save file:**
- Windows/Linux: `Ctrl + S`
- Mac: `Cmd + S`

**Open terminal:**
- Windows/Linux: `` Ctrl + ` ``
- Mac: `` Cmd + ` ``

**Open file quickly:**
- Windows/Linux: `Ctrl + P`
- Mac: `Cmd + P`

---

## Summary: What You Did

1. ✅ Installed VSCode
2. ✅ Installed Python
3. ✅ Downloaded the project from GitHub
4. ✅ Switched to the testing branch
5. ✅ Installed the Python extension
6. ✅ Created a virtual environment
7. ✅ Installed required packages
8. ✅ Configured VSCode to use the right Python
9. ✅ Created config.json with your API key
10. ✅ Verified everything works
11. ✅ Tested API access
12. ✅ Ran the program successfully!

**You're now a VSCode user! 🎉**

---

## Getting Help

**If you're stuck:**
1. Read the error message carefully - it usually tells you what's wrong
2. Check the "Common Issues & Solutions" section above
3. Make sure you followed every step in order
4. Try closing VSCode and starting fresh from where you got stuck

**Still stuck?**
- Check if you skipped any steps
- Make sure all files are saved
- Make sure virtual environment is activated (you see `(venv)`)
- Try restarting your computer and starting from Part 6

---

## You Did It! 🎊

If you made it here and the program ran successfully, you've:
- Learned how to use VSCode
- Learned how to use Git to download code
- Learned how to use Python virtual environments
- Learned how to run Python programs
- Successfully ran a real-world data collection tool!

**That's impressive for a beginner! Great work!** 👏
