# Pokimate

Personal finance and life management app for 1–3 users. Local-first, offline-first, with manual encrypted Google Drive sync and optional AI insights.

## Prerequisites

- **Backend**: Python 3.11+, pip
- **Web**: Node.js 18+, npm/pnpm
- **Mobile**: Node.js 18+, Expo CLI, Android Studio / Xcode (for simulators)
- **Desktop**: Rust toolchain, Node.js (for web build)
- **Optional**: Docker & Docker Compose

## Quick start (one-command run)

```bash
# Clone and enter repo (root folder = where README, backend/, web/, etc. live)
cd Pokimate

# Backend: install deps, run migrations, start server
make dev-backend
# Or: cd backend && pip install -e . && alembic upgrade head && uvicorn app.main:app --reload

# Web: install deps and run dev server
make dev-web
# Or: cd web && npm install && npm run dev

# Seed demo data (after backend is running)
curl -X POST http://localhost:8000/admin/seed-demo -H "Authorization: Bearer <admin_token>"
# Or use the web app: login as admin, then visit Settings > Seed demo data
```

- **Backend**: http://localhost:8000  
- **Web**: http://localhost:3000  
- **API docs**: http://localhost:8000/docs  

## Development setup

### Backend

```bash
cd backend
pip install -e ".[dev]"
cp ../.env.example .env   # edit .env with your values
alembic upgrade head
uvicorn app.main:app --reload
```

### Web

```bash
cd web
npm install
cp ../.env.example .env.local   # set NEXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
```

### Mobile (Expo)

```bash
cd mobile
npm install
# Set EXPO_PUBLIC_API_BASE to your machine's LAN IP (e.g. http://192.168.1.10:8000)
npx expo start
```

### Desktop (Tauri)

```bash
# Build web first: cd web && npm run build (or static export)
cd desktop
npm install
npx tauri dev
```

### Docker

```bash
make docker-up    # starts backend + web (+ optional ai_service)
make docker-down
```

## Seed / demo data

1. Start the backend and register the first user (they become ADMIN):  
   `POST /auth/register` with `{"email":"admin@example.com","username":"admin","password":"YourStrongPassword123!"}`.
2. Login to get a token: `POST /auth/login` with the same email and password.
3. Seed demo data: `POST /admin/seed-demo` with header `Authorization: Bearer <your_access_token>`.
4. Or from backend dir: `python -m app.utils.seed` (after creating a user and passing `--user-id 1` if needed).
5. After seeding, the dashboard shows meaningful KPIs and charts.

## Testing

```bash
make test-backend
# Or: cd backend && pytest -v
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API spec](docs/API_SPEC.md)
- [DB schema](docs/DB_SCHEMA.md)
- [Sync & security](docs/SYNC_SECURITY.md)
- [UI guide](docs/UI_GUIDE.md)
- [Runbook / debug](docs/RUNBOOK_DEBUG.md)
- [Roadmap](docs/ROADMAP.md)

## Git / GitHub

Initialize Git in the **repository root** (the folder that contains this README, `backend/`, `web/`, etc.). See [GIT_SETUP.md](GIT_SETUP.md) for step-by-step push instructions.

## Icons and logos

Placeholder icons (favicon and PWA icons) are in `web/public/favicon.svg` and `web/public/icons/`. Replace these with your own assets when ready.

## License

Private / personal use.
