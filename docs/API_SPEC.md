# Pokimate — API spec

Base URL: `http://localhost:8000` (or configured origin).

## Response shape

- Success: `{ "success": true, "data": <payload> }`
- Error: `{ "success": false, "error": "<message>" }` with appropriate HTTP status (4xx/5xx).

## Auth

### POST /auth/register

First user becomes ADMIN; thereafter admin-only or disabled.

**Request:** `{ "email": "...", "username": "...", "password": "..." }`  
**Response 201:** `{ "id": 1, "email": "...", "username": "...", "role": "ADMIN" }`

### POST /auth/login

**Request:**
```json
{ "email": "admin@example.com", "password": "StrongPassword123!" }
```

**Response 200:**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": { "id": 1, "email": "admin@example.com", "username": "admin", "role": "ADMIN" }
}
```

### POST /auth/refresh

**Body:** `{ "refresh_token": "<jwt>" }`  
**Response 200:** New access_token (and optionally refresh_token).

### POST /auth/logout

**Headers:** `Authorization: Bearer <access_token>`  
**Response 200:** Success.

### GET /auth/me

**Headers:** `Authorization: Bearer <access_token>`  
**Response 200:** Current user object.

---

## Health

### GET /health

**Response 200:** `{ "status": "ok" }` (or similar).

---

## Finance

### GET /finance/transactions

**Query:** `from`, `to` (YYYY-MM-DD), `type` (income|expense|transfer).  
**Response 200:** List of transactions.

### POST /finance/transactions

**Request:**
```json
{
  "date": "2026-03-01",
  "amount": 1500.00,
  "currency": "INR",
  "type": "expense",
  "account_id": 1,
  "category_id": 4,
  "description": "Groceries - supermarket"
}
```

**Response 201:**
```json
{
  "id": 101,
  "user_id": 1,
  "date": "2026-03-01",
  "amount": 1500.0,
  "currency": "INR",
  "type": "expense",
  "account_id": 1,
  "category_id": 4,
  "description": "Groceries - supermarket",
  "created_at": "2026-03-04T10:30:00Z",
  "updated_at": "2026-03-04T10:30:00Z"
}
```

### PUT /finance/transactions/{id}

**Body:** Same fields as create (partial OK). **Response 200:** Updated transaction.

### DELETE /finance/transactions/{id}

**Response 204:** No content.

### GET /finance/categories

**Response 200:** List of categories (user-scoped).

### POST /finance/categories

**Body:** `{ "name": "...", "kind": "income"|"expense"|"transfer", "color": "..." }`  
**Response 201:** Category.

### GET /finance/budgets?month=YYYY-MM

**Response 200:** Budgets for month with utilization.

### POST /finance/budgets

**Body:** `{ "category_id": 1, "month": "2026-03", "limit_amount": 12000 }`  
**Response 201:** Budget.

### GET /finance/recurring

**Response 200:** Recurring rules with next_due_date.

### POST /finance/recurring

**Body:** title, amount, currency, category_id, account_id, frequency, day_of_month?, next_due_date.  
**Response 201:** Recurring rule.

### POST /finance/import/csv

**Body:** multipart/form-data file + optional mapping.  
**Response 200:** Import result (count, errors).

### GET /finance/summary?month=YYYY-MM

**Response 200:**
```json
{
  "month": "2026-03",
  "income_total": 85000.0,
  "expense_total": 52000.0,
  "savings_rate": 0.3882,
  "top_categories": [
    { "category": "Rent", "amount": 18000.0 },
    { "category": "Food", "amount": 9000.0 }
  ],
  "budget_utilization": [
    { "category": "Food", "limit": 12000.0, "used": 9000.0, "pct": 0.75 }
  ]
}
```

---

## Debt

### GET /debt/list

**Response 200:** List of debts.

### POST /debt

**Body:** name, type, principal, interest_rate_apr, emi_monthly, start_date, tenure_months, remaining_balance, minimum_payment?  
**Response 201:** Debt.

### PUT /debt/{id}, DELETE /debt/{id}

Standard CRUD.

### POST /debt/payment

**Body:** debt_id, date, amount, notes?  
**Response 201:** Debt payment.

### GET /debt/summary

**Response 200:** Aggregates (total balance, total EMI, DTI, stress index).

### POST /debt/simulate?s=avalanche|snowball

**Request:**
```json
{ "as_of_date": "2026-03-01", "extra_payment_monthly": 3000.0 }
```

**Response 200:**
```json
{
  "strategy": "avalanche",
  "as_of_date": "2026-03-01",
  "extra_payment_monthly": 3000.0,
  "debt_free_date": "2028-07-01",
  "total_interest": 245000.0,
  "interest_saved_vs_minimum": 62000.0,
  "monthly_schedule": [
    { "month": "2026-03", "payment": 18000.0, "interest": 6200.0, "principal": 11800.0, "balance": 742000.0 }
  ]
}
```

---

## Investments

### GET /investments/holdings, POST /investments/holdings, PUT /investments/holdings/{id}, DELETE /investments/holdings/{id}

Standard CRUD for holdings.

### POST /investments/cashflow

**Body:** holding_id?, date, amount, currency, label.  
**Response 201:** Cashflow (for XIRR).

### GET /investments/summary

**Response 200:** Total value, cost basis, allocation summary.

### GET /investments/allocation

**Response 200:** Allocation by asset class (percentages).

### POST /investments/xirr

**Request:**
```json
{
  "cashflows": [
    { "date": "2024-01-01", "amount": -100000.0 },
    { "date": "2024-06-01", "amount": -10000.0 },
    { "date": "2026-03-01", "amount": 135000.0 }
  ]
}
```

**Response 200:**
```json
{ "xirr": 0.1374, "method": "newton-raphson", "iterations": 7 }
```

---

## Life

### GET /life/metrics?from=&to=

**Response 200:** List of life_metrics.

### POST /life/metrics

**Request:**
```json
{
  "date": "2026-03-04",
  "sleep_hours": 7.0,
  "work_hours": 8.5,
  "exercise_minutes": 30,
  "mood_score": 4
}
```

**Response 201:**
```json
{
  "id": 501,
  "date": "2026-03-04",
  "sleep_hours": 7.0,
  "work_hours": 8.5,
  "exercise_minutes": 30,
  "mood_score": 4
}
```

### PUT /life/metrics/{id}

**Response 200:** Updated metric.

### GET /life/habits, POST /life/habits, POST /life/habits/{id}/checkin

**Response:** Habit list or created/updated record.

### GET /life/summary?week=YYYY-WW

**Response 200:** Weekly aggregates (sleep avg, exercise total, mood avg).

---

## Goals

### GET /goals, POST /goals, PUT /goals/{id}, DELETE /goals/{id}

Standard CRUD. **POST /goals/{id}/progress**: body `{ "progress_value": 5000 }`.

---

## Sync

### GET /sync/status

**Response 200:** last_sync, device_id, backup_count, drive_connected?.

### POST /sync/oauth/start

**Response 200:** `{ "auth_url": "..." }`.

### GET /sync/oauth/callback

Query: `code`, `state`. Exchanges code for tokens; stores; redirect or JSON.

### POST /sync/backup/upload

**Request:**
```json
{ "passphrase": "<user-entered-passphrase>", "keep_versions": 10 }
```

**Response 200:**
```json
{
  "status": "uploaded",
  "backup_id": "backup_20260304T103200Z_<deviceid>",
  "drive_file_id": "<drive-id>",
  "created_at_utc": "2026-03-04T10:32:00Z"
}
```

### GET /sync/backup/list

**Response 200:** List of backups (id, created_at_utc, device_id).

### POST /sync/backup/download

**Body:** `{ "backup_id": "..." }`. **Response 200:** Encrypted blob + manifest (or URL).

### POST /sync/backup/restore

**Body:** backup_id, passphrase. **Response 200:** Restore result; local DB replaced.

---

## AI (when AI_MODE != OFF)

### POST /ai/weekly-summary

**Response 200:** `{ "summary": "...", "cached_at": "..." }`.

### POST /ai/spending-insights

**Response 200:** Narrative (no math).

### POST /ai/debt-coach

**Response 200:** Supportive commentary (no math).

### POST /ai/portfolio-commentary

**Response 200:** Informational text only.

---

All mutation endpoints require `Authorization: Bearer <access_token>`. Admin can access any user's data when implemented with an override.
