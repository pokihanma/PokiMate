# Pokimate — Runbook / debug

## Health checks

- **Backend**: `GET http://localhost:8000/health` → expect 200, `{ "status": "ok" }` (or similar).
- **Web**: Load http://localhost:3000; dashboard should load (or login).
- **DB**: Backend uses SQLite in `ASTRA_DB_DIR` (default `./data`). Ensure directory exists and is writable.

## Common issues

### Backend won’t start

- **Port 8000 in use**: Change port or stop other process: `netstat -ano | findstr :8000` (Windows), `lsof -i :8000` (macOS/Linux).
- **DB / migrations**: Run `alembic upgrade head` from `backend/`. If DB is missing, first run creates it (ensure ASTRA_DB_DIR exists).
- **Import errors**: Install deps: `pip install -e ".[dev]"` from backend.

### Web can’t reach API

- **CORS**: Ensure ASTRA_CORS_ORIGINS includes http://localhost:3000 (and 1420 for Tauri).
- **NEXT_PUBLIC_API_BASE**: Must be http://localhost:8000 (or your backend URL) in .env.local.

### Mobile can’t reach backend

- Use machine’s LAN IP (e.g. 192.168.1.x) in EXPO_PUBLIC_API_BASE, not localhost.
- Backend and phone on same network; firewall may block port 8000.

### Sync / Drive

- **OAuth**: Set ASTRA_GOOGLE_CLIENT_ID and ASTRA_GOOGLE_CLIENT_SECRET; redirect URI must match Google Console.
- **Offline mode**: When ASTRA_OFFLINE_MODE=true, sync endpoints return "offline mode enabled".

### AI not responding

- **AI_MODE=OFF**: AI routes disabled or return disabled; UI hides AI.
- **ai_service unreachable**: Backend falls back to "AI unavailable"; ensure ai_service URL in config if using FULL/LIGHT.

### Tests failing

- Run from backend: `pytest -v`. Ensure test DB or in-memory SQLite; no leftover state. Core tests: test_xirr, test_debt_sim, test_budget_math, test_encryption_roundtrip, test_health_scores.

## Logs

- Backend: uvicorn logs to stdout; increase log level in config if needed.
- Check sync_logs and audit_events in DB for sync and mutation history.
