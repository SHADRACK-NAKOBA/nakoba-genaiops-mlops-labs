# GenAIOps Lab 0 – Prerequisites: set up your computer

[🏠 Track home](../README.md) | [Next: Set up Microsoft Foundry ➡](01-setup-foundry.md)

**Goal:** install and check the 5 tools every GenAIOps lab uses. **Cost:** free. **Time:** 30–45 minutes.

| Tool | Used for |
|---|---|
| **Visual Studio Code** | Editing files and running commands (its built-in terminal) |
| **Python 3.12** (3.10–3.13 work) | Running the agent scripts |
| **Git** | Cloning your repo, commits, tags and branches |
| **Azure CLI** (`az`) | Signing in so Python can reach Azure |
| **Azure Developer CLI** (`azd`) | Creating the Foundry resources from the `infra` folder |

You also need:
- An **Azure subscription** where you are **Owner** (Free Trial works, and you are its Owner): https://azure.microsoft.com/free. *Contributor* alone isn't enough, because `azd up` gives you roles on the new resources.
- A **GitHub account**: https://github.com/signup

> No VM needed: install everything on your own computer.

---

## Option A – Windows, the fast way (winget)

1. Click **Start**, type **PowerShell**, right-click **Windows PowerShell** → **Run as administrator**.
2. Paste these lines one at a time (press **Enter** after each, and type **Y** if asked to accept terms):

   ```powershell
   winget install -e --id Microsoft.VisualStudioCode
   winget install -e --id Python.Python.3.12
   winget install -e --id Git.Git
   winget install -e --id Microsoft.AzureCLI
   winget install -e --id Microsoft.Azd
   ```
3. **Close all PowerShell and VS Code windows** (new tools only appear in new windows), then go to [Check everything](#check-everything).

> `winget` not found? Use Option B.

## Option B – Windows, by hand

### B1. Visual Studio Code
1. Go to https://code.visualstudio.com → **Download for Windows** → run the file.
2. Accept the agreement → **Next** → on *Select Additional Tasks* tick **Add "Open with Code" action** and **Add to PATH** → **Next** → **Install** → **Finish**.

### B2. Python
1. Go to https://www.python.org/downloads/ → download **Python 3.12.x** (Windows installer 64-bit).
2. Run it. On the **first screen**, tick **Add python.exe to PATH** (bottom of the window). ⚠️ This is the step most people miss.
3. Click **Install Now** → **Close**.
4. Turn off the fake "python" that opens the Microsoft Store: **Start** → type **Manage app execution aliases** → switch **off** *App Installer python.exe* and *python3.exe*.

### B3. Git
1. Go to https://git-scm.com/download/win → **64-bit Git for Windows Setup** → run it.
2. Click **Next** on every screen (the defaults are fine) → **Install** → **Finish**.

### B4. Azure CLI
1. Go to https://aka.ms/installazurecliwindowsx64 (downloads the latest 64-bit MSI) → run it.
2. Tick the agreement → **Install** → **Finish**.

### B5. Azure Developer CLI (azd)
1. Open **PowerShell** (normal, not admin) and run:
   ```powershell
   powershell -ex AllSigned -c "Invoke-RestMethod 'https://aka.ms/install-azd.ps1' | Invoke-Expression"
   ```
2. Close PowerShell when it finishes.

## Option C – macOS

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"   # skip if you have Homebrew
brew install --cask visual-studio-code
brew install python@3.12 git azure-cli
brew tap azure/azd && brew install azd
```
On a Mac, use `python3` wherever these labs say `python`.

---

## Check everything

Open a **new** VS Code window → menu **Terminal → New Terminal**, then run:

```bash
code --version
python --version
git --version
az --version
azd version
```

Each line must print a version number. `python --version` must say **3.10, 3.11, 3.12 or 3.13**.

| Problem | Fix |
|---|---|
| `... is not recognized` / `command not found` | Close **all** VS Code and terminal windows and open a new one. Still failing? Restart the computer. |
| `python` opens the Microsoft Store | Step B2.4 (turn off the app execution aliases), or reinstall Python with **Add python.exe to PATH** ticked |
| Python 3.14 or newer | Install 3.12 as well (`winget install -e --id Python.Python.3.12`) and use `py -3.12` instead of `python` when you create the virtual environment in Lab 1 |

## Configure Git (once)

In the terminal (use **your** name and the email of your GitHub account):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Recommended VS Code extensions

In VS Code click the **Extensions** icon (four squares, left bar), search and **Install**:
- **Python** (Microsoft)
- **Azure Tools** (Microsoft)
- **Rainbow CSV** (makes the scoring sheets in Lab 2 easy to read)

## ✅ Checklist

- [ ] All 5 version commands work in a new VS Code terminal
- [ ] Git name and email configured
- [ ] Azure subscription where you are **Owner**, and a GitHub account

[🏠 Track home](../README.md) | [Next: Set up Microsoft Foundry ➡](01-setup-foundry.md)
