# PetMed: Letting Classmates Join Live

The website and the API run on one laptop (the "host"). Classmates open a link on their phone or laptop, then sign up or sign in. Everything they do is saved in the host's MySQL database.

The website forwards every `/api` request to the API (see `frontend/vite.config.js`), so **only the website needs to be shared**. The API and MySQL stay private on the host laptop.

## On the host laptop (do this first)

In two terminals, from the PetMed folder:

```powershell
python src/app.py
```

```powershell
cd frontend
npm.cmd run dev
```

## Option A: same Wi-Fi (simplest)

When `npm.cmd run dev` starts, it prints two addresses:

```
➜  Local:   http://localhost:5173/
➜  Network: http://192.168.1.25:5173/
```

1. Share the **Network** address (your numbers will differ). Classmates on the **same Wi-Fi** open it.
2. If Windows Firewall asks about Node.js, allow it on **Private networks**.

Campus Wi-Fi (eduroam) often blocks devices from reaching each other. If classmates can't open the Network address, use Option B.

## Option B: a public link with Cloudflare (works anywhere)

Cloudflare's free quick tunnel gives your local site a temporary `https://` link that anyone can open. No account is needed.

1. Install it once, in PowerShell:

   ```powershell
   winget install --id Cloudflare.cloudflared
   ```

   Close and reopen the terminal afterward.

2. With the website running, open a third terminal and run:

   ```powershell
   cloudflared tunnel --url http://localhost:5173
   ```

3. It prints a link like `https://random-words-here.trycloudflare.com`. Share that link, for example as a QR code on the screen. Classmates open it, click **Sign Up**, and create an account.

4. When the demo is over, press **Ctrl + C** in the Cloudflare terminal. The link stops working right away.

A new link is created every time you start the tunnel.

## Before and after sharing

- **Anyone with the link can use the site.** The sample accounts share the demo password `PetMed123!`, which is written in the repo, so anyone who knows it could sign in as the Administrator. Share the link only during the demo, and stop the tunnel right after.
- **Tell classmates not to reuse a real password** when they sign up. Use something like `Pets2026`.
- **Afterward, rebuild the database** with the five scripts (`src/README.md`, step 1). That removes the classmates' accounts. The tests expect exactly 8 users, so they fail until you rebuild.
- The API's debug mode is off by default, so error details are never shown to visitors. For local debugging only, start it with `$env:PETMED_DEBUG="1"; python src/app.py`.
