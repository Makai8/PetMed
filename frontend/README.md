# Running the PetMed Sprint 1 Splash Screen

The React application is located at:

```text
frontend/sprint_1_splashscreen
```

Before running the project, make sure Node.js and npm are installed.

Check Node.js:

```bash
node --version
```

Check npm:

```bash
npm --version
```

If either command is not recognized, install the LTS version of Node.js from:

```text
https://nodejs.org/
```

npm is included with Node.js.

---

# Git Bash Instructions

Open Git Bash inside the main PetMed repository folder.

## Step 1 - Pull the latest version from GitHub

```bash
git pull origin main
```

## Step 2 - Go to the Sprint 1 splash screen

```bash
cd frontend/sprint_1_splashscreen
```

## Step 3 - Confirm the project files are present

```bash
pwd
ls
```

You should see:

```text
package.json
public/
src/
README.md
```

## Step 4 - Install the required packages

```bash
npm install
```

The first installation may take several minutes.

Warnings may appear during installation. If the installation completes successfully, continue to the next step.

## Step 5 - Start the React application

```bash
npm start
```

A successful start should display:

```text
Compiled successfully!

You can now view petmed-frontend in the browser.

Local: http://localhost:3000
```

Open:

```text
http://localhost:3000
```

in your browser.

## Git Bash - Full Copy-and-Paste Commands

```bash
git pull origin main
cd frontend/sprint_1_splashscreen
pwd
ls
npm install
npm start
```

## Git Bash - Quick Start After Dependencies Are Installed

After `npm install` has already been completed once:

```bash
git pull origin main
cd frontend/sprint_1_splashscreen
npm start
```

To stop the development server, press:

```text
Ctrl + C
```

---

# PowerShell Instructions

Open PowerShell inside the main PetMed repository folder.

## Step 1 - Pull the latest version from GitHub

```powershell
git pull origin main
```

## Step 2 - Go to the Sprint 1 splash screen

```powershell
cd frontend\sprint_1_splashscreen
```

## Step 3 - Confirm the project files are present

```powershell
Get-Location
Get-ChildItem
```

You should see:

```text
package.json
public
src
README.md
```

## Step 4 - Install the required packages

```powershell
npm install
```

Wait for the installation to finish.

## Step 5 - Start the React application

```powershell
npm start
```

A successful start should display:

```text
Compiled successfully!

You can now view petmed-frontend in the browser.

Local: http://localhost:3000
```

Open:

```text
http://localhost:3000
```

in your browser.

## PowerShell - Full Copy-and-Paste Commands

```powershell
git pull origin main
cd frontend\sprint_1_splashscreen
Get-Location
Get-ChildItem
npm install
npm start
```

## PowerShell - Quick Start After Dependencies Are Installed

```powershell
git pull origin main
cd frontend\sprint_1_splashscreen
npm start
```

To stop the development server, press:

```text
Ctrl + C
```

---

# Troubleshooting

## package.json Not Found

If you receive an error similar to:

```text
npm error code ENOENT
npm error enoent Could not read package.json
```

you are probably running npm from the wrong folder.

The correct project folder is:

```text
frontend/sprint_1_splashscreen
```

### Git Bash

```bash
cd frontend/sprint_1_splashscreen
ls
```

### PowerShell

```powershell
cd frontend\sprint_1_splashscreen
Get-ChildItem
```

Make sure `package.json` appears before running:

```bash
npm install
npm start
```

---

# Git Bash Path Note

Git Bash uses forward slashes.

Windows path:

```text
C:\Users\YourName\GitHub\PetMed
```

Git Bash equivalent:

```text
/c/Users/YourName/GitHub/PetMed
```

If Git Bash is already opened inside the PetMed repository, you do not need to type the full computer-specific path.

You can simply run:

```bash
git pull origin main
cd frontend/sprint_1_splashscreen
npm install
npm start
```

---

# Sprint Cycle I Verification

The PetMed React splash screen was successfully tested using:

```bash
npm install
npm start
```

The development server returned:

```text
Compiled successfully!
```

and the application was available at:

```text
http://localhost:3000
```

This verifies that the React frontend environment is working correctly.


# I an error Still occures run this 

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

### Then 

npm install
npm start