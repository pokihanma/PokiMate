from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.models import (
    User,
    Account,
    Category,
    Transaction,
    Budget,
    RecurringRule,
    Debt,
    DebtPayment,
    Holding,
    InvestmentCashflow,
    LifeMetric,
    Habit,
    HabitEntry,
    Goal,
    SyncLog,
    AuditEvent,
)
from app.routes import health, auth, finance, debt, investments, life, goals, sync, ai, admin


@asynccontextmanager
def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Pokimate API", version="0.1.0", lifespan=lifespan)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(finance.router)
app.include_router(debt.router)
app.include_router(investments.router)
app.include_router(life.router)
app.include_router(goals.router)
app.include_router(sync.router)
app.include_router(ai.router)
app.include_router(admin.router)
