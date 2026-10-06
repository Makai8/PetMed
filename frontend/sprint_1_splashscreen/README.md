# PetMed Frontend — Sprint Cycle I

This folder contains the **Sprint Cycle I technical proof-of-concept splash/home screen** for PetMed.

The screen intentionally does **not** implement authentication, database access, user roles, or the major PetMed use cases. Its purpose is to verify that the team's React development environment and GitHub workflow are working.

## Requirements

Install the following before running the project:

- Node.js
- npm
- Git
- Visual Studio Code (recommended)

## Run the application

From the repository root:

```bash
cd frontend
npm install
npm start
```

The development server should open PetMed in a browser, normally at:

```text
http://localhost:3000
```

To stop the development server, press `Ctrl + C` in the terminal.

## What the Sprint I home screen includes

- PetMed application name
- PetMed paw/logo placeholder
- Short project tagline and description
- Placeholder navigation for Login, About, Help, and Contact Us
- Basic responsive CSS styling
- Decorative application-preview graphic

The navigation items and buttons are placeholders and are not expected to work during Sprint Cycle I.

## Verify the project after pulling from GitHub

Each team member should run:

```bash
git pull origin main
cd frontend
npm install
npm start
```

Confirm that the splash/home screen loads successfully on the local computer.

## Suggested Git workflow

Before editing:

```bash
git pull origin main
```

After making a meaningful Sprint I contribution:

```bash
git add .
git commit -m "Add Sprint Cycle I frontend contribution"
git push origin main
```

Each team member should commit from their own GitHub account.
