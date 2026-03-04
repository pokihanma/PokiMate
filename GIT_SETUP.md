# Git and GitHub setup

## Where to add Git (repo root)

**Use the project root folder** — the folder that contains:

- `README.md`
- `docker-compose.yml`
- `Makefile`
- `.env.example`
- `backend/`
- `web/`
- `mobile/`
- `desktop/`
- `ai_service/`
- `docs/`

That folder is your **repository root**. Initialize Git there and push from there.

### If your folder is still named AstraLife

1. **Rename the folder to Pokimate** (optional but matches the app name):
   - Close Cursor/IDE if the folder is open.
   - In File Explorer: right‑click `AstraLife` → Rename → `Pokimate`.
   - Or in PowerShell (run from `c:\Users\sudhakas\source\repos`):
     ```powershell
     Rename-Item -Path "AstraLife" -NewName "Pokimate"
     ```

2. **Initialize Git in the root folder** (after opening the renamed folder in Cursor, or from Explorer):

   ```powershell
   cd c:\Users\sudhakas\source\repos\Pokimate
   # Or if you didn't rename: cd c:\Users\sudhakas\source\repos\AstraLife

   git init
   git add .
   git commit -m "Initial commit: Pokimate"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your GitHub username and repository name.

### Summary

| Purpose              | Folder path (example)                         |
|----------------------|-----------------------------------------------|
| Git repo root        | `c:\Users\sudhakas\source\repos\Pokimate`      |
| Run `git init` here  | Yes — this folder                             |
| Do not run git init  | Inside `backend/`, `web/`, `mobile/`, etc.    |

One repository = one root. All apps (backend, web, mobile, desktop, ai_service) live in that single repo and get pushed together to GitHub.
