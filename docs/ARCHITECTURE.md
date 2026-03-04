# Pokimate — Architecture

## High-level overview

Pokimate is a local-first personal finance and life app. A single FastAPI backend exposes REST APIs; web (Next.js), mobile (Expo), and desktop (Tauri) clients consume them. Data lives in SQLite. Optional manual encrypted backup to Google Drive; optional AI insights via a small ai_service.

- **No SaaS infra**: No Kubernetes, message brokers, or managed DBs. Everything runs locally with optional Drive sync.

## Component diagram

```mermaid
flowchart LR
  subgraph clients [Clients]
    Web[Next.js PWA]
    Mobile[Expo RN]
    Desktop[Tauri]
  end
  subgraph backend [Backend]
    API[FastAPI REST]
    SQLite[(SQLite)]
    Engines[Finance/Debt/Invest/Life Engines]
  end
  subgraph optional [Optional]
    AIService[ai_service]
    Drive[Google Drive]
  end
  Web --> API
  Mobile --> API
  Desktop --> API
  API --> SQLite
  API --> Engines
  API --> AIService
  API --> Drive
```

## Local topology

- Backend: `http://localhost:8000`
- Web dev: `http://localhost:3000`
- Desktop: embeds built web UI; can auto-start backend on port 8000
- Mobile (dev): connects to backend via LAN IP (e.g. `http://192.168.1.x:8000`); offline cache for reads

## Data flow: transaction create

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant DB
  participant Audit
  participant Cache
  Client->>API: POST /finance/transactions
  API->>DB: insert transaction
  API->>Audit: append audit_event
  API->>Cache: invalidate or on-read
  API->>Client: 201 + transaction
```

1. Client sends create request.
2. API validates, applies RBAC (user_id), inserts into `transactions`.
3. API appends to `audit_events` (event_type, entity, old/new JSON, actor, device_id, timestamp).
4. Caches (e.g. summary/budget) are invalidated or recomputed on next read.
5. Response returned; UI updates.

## Sync flow

```mermaid
sequenceDiagram
  participant User
  participant Backend
  participant Encrypt
  participant Drive
  User->>Backend: POST /sync/backup/upload (passphrase)
  Backend->>Backend: snapshot DB file
  Backend->>Encrypt: AES-256-GCM (key from Argon2id)
  Backend->>Drive: upload .enc + manifest
  Backend->>Backend: sync_log
  Backend->>User: 200 backup_id
```

**Restore**: User selects backup → Backend downloads from Drive → verify SHA-256 → decrypt with passphrase → atomic replace local DB → sync_log → reload.

## AI flow

```mermaid
sequenceDiagram
  participant Client
  participant Backend
  participant Cache
  participant AIService
  Client->>Backend: POST /ai/weekly-summary
  Backend->>Backend: build sanitized payload (KPIs, categories, goals)
  Backend->>Cache: get(key = hash(payload+version+mode))
  alt cache hit
    Cache->>Backend: cached response
  else cache miss
    Backend->>AIService: POST /ai/summarize
    AIService->>Backend: narrative (no math)
    Backend->>Cache: set(key, response, TTL)
  end
  Backend->>Client: 200 + insight
```

- AI never does math; all calculations are deterministic in backend engines.
- Cache key: `hash(payload + prompt_version + ai_mode)`; TTL e.g. 7 days for weekly, 1 day for daily.

## Database strategy

- **Option A**: Single SQLite DB with `user_id` on every table. Strict RBAC in code; all queries filtered by current user (or admin override).
- Sync: one file to encrypt and upload; restore replaces that file.

## Rationale: no SaaS

- Target is 1–3 users, personal use.
- Local-first and offline-first require local DB and optional sync, not a central cloud DB.
- Avoiding managed infra keeps setup simple and cost-free.
