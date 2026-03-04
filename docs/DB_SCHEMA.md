# Pokimate — Database schema

Single SQLite database; all tables have `user_id` (FK to users) except `users`. Foreign keys enabled. Indexes and constraints as below.

---

## users

| Column         | Type     | Constraints |
|----------------|----------|-------------|
| id             | INTEGER  | PK          |
| username       | TEXT     | UNIQUE      |
| email          | TEXT     | UNIQUE      |
| password_hash  | TEXT     |             |
| role           | TEXT     | ADMIN, USER |
| created_at     | DATETIME |             |
| updated_at     | DATETIME |             |

**Indices:** email, username

---

## accounts

| Column          | Type     | Constraints |
|-----------------|----------|-------------|
| id              | INTEGER  | PK          |
| user_id         | INTEGER  | FK users.id |
| name            | TEXT     |             |
| type            | TEXT     | cash, bank, credit, wallet |
| currency        | TEXT     | default INR |
| opening_balance | DECIMAL  |             |
| created_at      | DATETIME |             |

**Indices:** user_id, type

---

## categories

| Column    | Type     | Constraints |
|-----------|----------|-------------|
| id        | INTEGER  | PK          |
| user_id   | INTEGER  | FK users.id |
| name      | TEXT     |             |
| kind      | TEXT     | income, expense, transfer |
| color     | TEXT     | optional    |
| keywords  | TEXT     | optional JSON array |
| created_at| DATETIME |             |

**Indices:** user_id, kind, name

---

## transactions

| Column        | Type     | Constraints |
|---------------|----------|-------------|
| id            | INTEGER  | PK          |
| user_id       | INTEGER  | FK users.id |
| date          | DATE     | YYYY-MM-DD  |
| amount        | DECIMAL  |             |
| currency      | TEXT     | INR         |
| type          | TEXT     | income, expense, transfer |
| account_id    | INTEGER  | FK accounts.id |
| to_account_id | INTEGER  | FK, nullable (transfer) |
| category_id   | INTEGER  | FK categories.id |
| description   | TEXT     |             |
| merchant      | TEXT     | optional    |
| notes         | TEXT     | optional    |
| created_at    | DATETIME |             |
| updated_at    | DATETIME |             |

**Indices:** (user_id, date), (user_id, type), (user_id, category_id)  
**Constraint:** type IN (income, expense, transfer)

---

## budgets

| Column       | Type     | Constraints |
|--------------|----------|-------------|
| id           | INTEGER  | PK          |
| user_id      | INTEGER  | FK users.id |
| category_id  | INTEGER  | FK categories.id |
| period       | TEXT     | monthly     |
| month        | TEXT     | YYYY-MM     |
| limit_amount | DECIMAL  |             |
| created_at   | DATETIME |             |

**Indices:** (user_id, month)

---

## recurring_rules

| Column        | Type     | Constraints |
|---------------|----------|-------------|
| id            | INTEGER  | PK          |
| user_id       | INTEGER  | FK users.id |
| title         | TEXT     |             |
| amount        | DECIMAL  |             |
| currency      | TEXT     |             |
| category_id   | INTEGER  | FK          |
| account_id    | INTEGER  | FK          |
| frequency     | TEXT     | weekly, monthly, yearly |
| day_of_month  | INTEGER  | nullable    |
| next_due_date | DATE     |             |
| is_active     | BOOLEAN  |             |
| created_at    | DATETIME |             |

**Indices:** (user_id, next_due_date)

---

## debts

| Column             | Type     | Constraints |
|--------------------|----------|-------------|
| id                 | INTEGER  | PK          |
| user_id            | INTEGER  | FK users.id |
| name               | TEXT     |             |
| type               | TEXT     | credit_card, loan, other |
| principal          | DECIMAL  |             |
| interest_rate_apr  | DECIMAL  |             |
| emi_monthly        | DECIMAL  |             |
| start_date         | DATE     |             |
| tenure_months      | INTEGER  |             |
| remaining_balance  | DECIMAL  |             |
| minimum_payment    | DECIMAL  | optional    |
| created_at         | DATETIME |             |

**Indices:** user_id, remaining_balance

---

## debt_payments

| Column   | Type     | Constraints |
|----------|----------|-------------|
| id       | INTEGER  | PK          |
| user_id  | INTEGER  | FK users.id |
| debt_id  | INTEGER  | FK debts.id |
| date     | DATE     |             |
| amount   | DECIMAL  |             |
| notes    | TEXT     |             |

**Indices:** (user_id, date), debt_id

---

## investments_holdings (or holdings)

| Column         | Type     | Constraints |
|----------------|----------|-------------|
| id             | INTEGER  | PK          |
| user_id        | INTEGER  | FK users.id |
| type           | TEXT     | stock, mf, sip, gold, fd, mmf |
| asset_name     | TEXT     |             |
| units          | DECIMAL  |             |
| avg_cost       | DECIMAL  |             |
| current_price  | DECIMAL  |             |
| currency       | TEXT     |             |
| as_of_date     | DATE     |             |
| created_at     | DATETIME |             |

**Indices:** (user_id, type), asset_name

---

## investment_cashflows

| Column     | Type     | Constraints |
|------------|----------|-------------|
| id         | INTEGER  | PK          |
| user_id    | INTEGER  | FK users.id |
| holding_id | INTEGER  | FK, nullable |
| date       | DATE     |             |
| amount     | DECIMAL  |             |
| currency   | TEXT     |             |
| label      | TEXT     |             |

**Indices:** (user_id, date)

---

## life_metrics

| Column           | Type     | Constraints |
|------------------|----------|-------------|
| id               | INTEGER  | PK          |
| user_id          | INTEGER  | FK users.id |
| date             | DATE     |             |
| sleep_hours      | DECIMAL  |             |
| work_hours       | DECIMAL  |             |
| exercise_minutes | INTEGER  |             |
| mood_score       | INTEGER  | 1-5         |
| notes            | TEXT     | optional    |

**Indices:** (user_id, date) UNIQUE

---

## habits

| Column      | Type     | Constraints |
|-------------|----------|-------------|
| id          | INTEGER  | PK          |
| user_id     | INTEGER  | FK users.id |
| title       | TEXT     |             |
| description | TEXT     |             |
| frequency   | TEXT     | daily, weekly |
| is_active   | BOOLEAN  |             |
| created_at  | DATETIME |             |

**Indices:** (user_id, is_active)

---

## habit_entries

| Column    | Type     | Constraints |
|-----------|----------|-------------|
| id        | INTEGER  | PK          |
| user_id   | INTEGER  | FK users.id |
| habit_id  | INTEGER  | FK habits.id |
| date      | DATE     |             |
| completed | BOOLEAN  |             |

**Indices:** (habit_id, date) UNIQUE

---

## goals

| Column        | Type     | Constraints |
|---------------|----------|-------------|
| id            | INTEGER  | PK          |
| user_id       | INTEGER  | FK users.id |
| type          | TEXT     | savings, fitness, habit, other |
| title         | TEXT     |             |
| description   | TEXT     |             |
| target_date   | DATE     |             |
| target_value  | DECIMAL  | optional    |
| progress_value| DECIMAL  | optional    |
| status        | TEXT     | active, paused, done |
| created_at    | DATETIME |             |

**Indices:** (user_id, status), (user_id, target_date)

---

## sync_logs

| Column    | Type     | Constraints |
|-----------|----------|-------------|
| id        | INTEGER  | PK          |
| user_id   | INTEGER  | FK users.id |
| direction | TEXT     | upload, download, restore |
| status    | TEXT     | success, fail |
| backup_id | TEXT     |             |
| device_id | TEXT     |             |
| timestamp | DATETIME |             |
| message   | TEXT     |             |

**Indices:** (user_id, timestamp)

---

## audit_events (append-only)

| Column        | Type     | Constraints |
|---------------|----------|-------------|
| id            | INTEGER  | PK          |
| user_id       | INTEGER  | FK users.id |
| actor_user_id | INTEGER  |             |
| device_id     | TEXT     |             |
| event_type    | TEXT     | create, update, delete, restore, import |
| entity        | TEXT     | transaction, debt, holding, ... |
| entity_id     | INTEGER  |             |
| old_json      | TEXT     |             |
| new_json      | TEXT     |             |
| timestamp     | DATETIME |             |

**Indices:** (user_id, timestamp), (entity, entity_id)
