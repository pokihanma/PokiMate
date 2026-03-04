"""Seed demo data: 3 months transactions, 2 debts, 4 holdings, 14 days life metrics, 3 habits, 2 goals."""
from datetime import date, timedelta
from decimal import Decimal
from sqlmodel import Session
from app.models.user import User
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.debt import Debt
from app.models.holding import Holding
from app.models.life_metric import LifeMetric
from app.models.habit import Habit
from app.models.habit_entry import HabitEntry
from app.models.goal import Goal


def run_seed(session: Session, user_id: int) -> None:
    # Default accounts
    acc_cash = Account(user_id=user_id, name="Cash", type="cash", currency="INR", opening_balance=Decimal("5000"))
    acc_bank = Account(user_id=user_id, name="Main Bank", type="bank", currency="INR", opening_balance=Decimal("100000"))
    session.add(acc_cash)
    session.add(acc_bank)
    session.commit()
    session.refresh(acc_cash)
    session.refresh(acc_bank)
    aid_cash, aid_bank = acc_cash.id, acc_bank.id

    # Default categories
    cat_income = Category(user_id=user_id, name="Salary", kind="income")
    cat_rent = Category(user_id=user_id, name="Rent", kind="expense")
    cat_food = Category(user_id=user_id, name="Food", kind="expense")
    cat_grocery = Category(user_id=user_id, name="Groceries", kind="expense")
    session.add(cat_income)
    session.add(cat_rent)
    session.add(cat_food)
    session.add(cat_grocery)
    session.commit()
    for c in [cat_income, cat_rent, cat_food, cat_grocery]:
        session.refresh(c)
    cid_income, cid_rent, cid_food, cid_grocery = cat_income.id, cat_rent.id, cat_food.id, cat_grocery.id

    # 3 months transactions
    base = date.today().replace(day=1) - timedelta(days=90)
    for m in range(3):
        month_start = base.replace(day=1) + timedelta(days=m * 30)
        session.add(Transaction(user_id=user_id, date=month_start, amount=Decimal("85000"), currency="INR", type="income", account_id=aid_bank, category_id=cid_income, description="Salary"))
        session.add(Transaction(user_id=user_id, date=month_start + timedelta(days=2), amount=Decimal("18000"), currency="INR", type="expense", account_id=aid_bank, category_id=cid_rent, description="Rent"))
        session.add(Transaction(user_id=user_id, date=month_start + timedelta(days=5), amount=Decimal("4500"), currency="INR", type="expense", account_id=aid_bank, category_id=cid_food, description="Dining"))
        session.add(Transaction(user_id=user_id, date=month_start + timedelta(days=10), amount=Decimal("3200"), currency="INR", type="expense", account_id=aid_bank, category_id=cid_grocery, description="Groceries"))
    session.commit()

    # 2 debts
    d1 = Debt(user_id=user_id, name="Personal Loan", type="loan", principal=Decimal("500000"), interest_rate_apr=Decimal("12"), emi_monthly=Decimal("12000"), start_date=base, tenure_months=48, remaining_balance=Decimal("420000"))
    d2 = Debt(user_id=user_id, name="Credit Card", type="credit_card", principal=Decimal("50000"), interest_rate_apr=Decimal("24"), emi_monthly=Decimal("5000"), start_date=base, tenure_months=12, remaining_balance=Decimal("35000"))
    session.add(d1)
    session.add(d2)
    session.commit()

    # 4 holdings
    h1 = Holding(user_id=user_id, type="mf", asset_name="Index Fund", units=Decimal("100"), avg_cost=Decimal("150"), current_price=Decimal("165"), currency="INR", as_of_date=date.today())
    h2 = Holding(user_id=user_id, type="stock", asset_name="Equity A", units=Decimal("50"), avg_cost=Decimal("800"), current_price=Decimal("920"), currency="INR", as_of_date=date.today())
    h3 = Holding(user_id=user_id, type="fd", asset_name="FD Bank", units=Decimal("1"), avg_cost=Decimal("100000"), current_price=Decimal("105000"), currency="INR", as_of_date=date.today())
    h4 = Holding(user_id=user_id, type="mmf", asset_name="Liquid Fund", units=Decimal("5000"), avg_cost=Decimal("1"), current_price=Decimal("1.02"), currency="INR", as_of_date=date.today())
    session.add(h1)
    session.add(h2)
    session.add(h3)
    session.add(h4)
    session.commit()

    # 14 days life metrics
    for i in range(14):
        d = date.today() - timedelta(days=i)
        session.add(LifeMetric(user_id=user_id, date=d, sleep_hours=Decimal("7"), work_hours=Decimal("8"), exercise_minutes=30, mood_score=4))
    session.commit()

    # 3 habits
    hab1 = Habit(user_id=user_id, title="Morning run", frequency="daily")
    hab2 = Habit(user_id=user_id, title="Read 30 min", frequency="daily")
    hab3 = Habit(user_id=user_id, title="Weekly review", frequency="weekly")
    session.add(hab1)
    session.add(hab2)
    session.add(hab3)
    session.commit()
    session.refresh(hab1)
    session.refresh(hab2)
    session.refresh(hab3)
    for i in range(7):
        session.add(HabitEntry(user_id=user_id, habit_id=hab1.id, date=date.today() - timedelta(days=i), completed=True))
    session.commit()

    # 2 goals
    g1 = Goal(user_id=user_id, type="savings", title="Emergency fund", target_date=date.today() + timedelta(days=365), target_value=Decimal("300000"), progress_value=Decimal("80000"), status="active")
    g2 = Goal(user_id=user_id, type="fitness", title="Run 5K", target_date=date.today() + timedelta(days=90), status="active")
    session.add(g1)
    session.add(g2)
    session.commit()
