## Database Setup (MySQL)

PetMed uses a **MySQL** database named `petmed`. The full schema (41 tables, 69 foreign keys and the business-rule checks) is in [`backend/PetMedDB.sql`](backend/PetMedDB.sql) and matches the Sprint 2 ERD.

### 1. Install the tools

| Tool | Notes |
|---|---|
| **MySQL Server 26.10** (Community) | Download the Windows MSI from [dev.mysql.com/downloads/mysql](https://dev.mysql.com/downloads/mysql/). Choose **Typical**, keep port **3306**, set a **root password**, and leave "Configure as a Windows Service" checked. |
| **VS Code extensions** | **SQLTools** (`mtxr.sqltools`) and **SQLTools MySQL/MariaDB/TiDB** (`mtxr.sqltools-driver-mysql`). VS Code offers to install both when you open this repo. |

### 2. Add MySQL to your PATH (one time)

Run this in PowerShell, then restart VS Code:

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\MySQL\MySQL Server 26.10\bin", "User")
```

### 3. Save your login (one time)

This stores your password in an encrypted file on your own computer, so you aren't asked for it each time:

```powershell
mysql_config_editor set --login-path=petmed --user=root --password
```

### 4. Create the database

From the `backend` folder:

```powershell
Get-Content .\PetMedDB.sql -Raw | mysql --login-path=petmed
```

No output means it worked. Re-running the script after a design change? Drop the old copy first with `mysql --login-path=petmed -e "DROP DATABASE petmed;"`. This deletes any data in it.

### 5. Verify

```powershell
mysql --login-path=petmed -e "SELECT COUNT(*) AS tables FROM information_schema.tables WHERE table_schema='petmed';"
```

It should print **41**. To open a prompt inside the database, run `mysql --login-path=petmed petmed`, and type `exit` to leave.

### 6. Browse it in VS Code

Open the **SQLTools** sidebar and connect with **PetMed local**, which is defined in `.vscode/settings.json` and asks for your own password. To set up your own connection instead, use host `localhost`, port `3306`, database `petmed` and user `root`.

### ID numbering

Primary keys auto-increment. Two tables start at numbers that spell the table name on a phone keypad:

| Table | First ID | Keypad |
|---|---|---|
| `User` | **87370000** | U-S-E-R = 8-7-3-7 |
| `Pet` | **7380000** | P-E-T = 7-3-8 |

All other tables start at 1.

### Sharing data with the team

Each member runs their own local copy from `PetMedDB.sql`. To share test data, export it and commit the file:

```powershell
mysqldump --login-path=petmed --databases petmed --result-file=petmed_dump.sql
```

Use `--result-file` rather than `>`: PowerShell's `>` saves the file in an encoding MySQL can't import.

### Notes

- On Windows, MySQL stores table names in lowercase (`user`, `pet`). Queries work with any casing, but use the same casing as the schema so the code also runs on macOS and Linux.
- **Never commit passwords.** Keep `askForPassword: true` in the shared SQLTools connection.
- The schema requires **MySQL 8.0.16 or later**, because the business-rule `CHECK` constraints need it.