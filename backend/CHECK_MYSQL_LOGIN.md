# Check your MySQL login

Open this project in VS Code, then choose **Terminal > New Terminal** and use PowerShell.

## 1. Check saved logins

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql_config_editor.exe" print --all
```

This shows saved login names, usernames, and hosts. Passwords stay hidden. Look for a `[petmed]` entry.

## 2. Test the saved PetMed login

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" --login-path=petmed -e "SHOW DATABASES;"
```

A database list means the login works. Look for `petmed` in the list.

## 3. If no saved login exists, test root directly

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Enter the password you chose when installing MySQL. Nothing appears while typing the password; this is normal. A `mysql>` prompt means the login worked.

At that prompt, check the database:

```sql
SHOW DATABASES;
USE petmed;
SHOW TABLES;
exit
```

## 4. Save a working root login as petmed

After confirming that your root password works, run this in PowerShell:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql_config_editor.exe" set --login-path=petmed --host=localhost --user=root --password
```

Enter your password when prompted, then repeat step 2. This creates or updates the saved `petmed` login on your computer.

## Common results

- **Access denied:** Check the username and password. An error mentioning `ODBC` and `using password: NO` indicates the intended saved login was not applied.
- **Cannot connect:** Check that the MySQL Windows service is running.
- **Unknown database 'petmed':** The login works, but the project database still needs to be created.
- **Executable path not found:** Check the installed MySQL folder under `C:\Program Files\MySQL` and adjust the commands.

Do not put passwords in this file, SQL scripts, or GitHub. Share only output or error messages with passwords removed.
