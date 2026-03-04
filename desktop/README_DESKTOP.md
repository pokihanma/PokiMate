# Pokimate Desktop

Tauri 2 wrapper for the Pokimate web app. Provides system tray (Open, Sync now, Add transaction, Quit) and optional backend auto-start.

## Prerequisites

- Rust toolchain (rustup)
- Node.js (for building web frontend when using custom build)
- Backend and web app (see root README)

## Development

1. Start the backend: `cd backend && uvicorn app.main:app --reload`
2. Start the web dev server: `cd web && npm run dev`
3. Run desktop: `cd desktop && npm run dev` (or `npx tauri dev`)

In dev, the app loads `http://localhost:3000`. The tray menu is available from the system tray.

## Backend auto-start

The app can try to start the backend if it is not running on port 8000. Use the `cmd_ensure_backend` invoke from the frontend, or configure startup logic in `src-tauri/src/backend.rs`. Backend path is resolved relative to the desktop executable (sibling `backend/` directory).

## Windows build

1. Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and WebView2.
2. From repo root, build web: `cd web && npm run build` (ensure Next.js outputs to `out` for static export, or point `frontendDist` in `tauri.conf.json` to your build output).
3. Build desktop: `cd desktop && npx tauri build`.
4. Installer and binary will be in `desktop/src-tauri/target/release/`.

## Notifications

Stubs for budget exceeded, upcoming recurring, and goal milestone are in `src-tauri/src/notifications.rs`. Wire them to Tauri's notification API when needed.
