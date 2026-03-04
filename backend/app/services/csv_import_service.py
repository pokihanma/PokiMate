"""CSV import for transactions. Returns count and errors."""
import csv
import io
from datetime import datetime
from decimal import Decimal
from sqlmodel import Session
from app.models.transaction import Transaction
from app.utils.validation import transaction_type_valid


def parse_row(row: dict, user_id: int, account_id: int, category_id: int) -> dict | str:
    """Parse one row to transaction dict or error string."""
    try:
        date_str = row.get("date", "").strip()
        date_val = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        try:
            date_val = datetime.strptime(date_str, "%d/%m/%Y").date()
        except (ValueError, TypeError):
            return f"Invalid date: {date_str}"
    try:
        amount = Decimal(str(row.get("amount", 0)).replace(",", ""))
    except Exception:
        return "Invalid amount"
    ttype = (row.get("type", "expense") or "expense").strip().lower()
    if not transaction_type_valid(ttype):
        return f"Invalid type: {ttype}"
    return {
        "user_id": user_id,
        "date": date_val,
        "amount": amount,
        "currency": row.get("currency", "INR"),
        "type": ttype,
        "account_id": account_id,
        "category_id": category_id,
        "description": (row.get("description") or "")[:500],
    }


def import_csv(
    session: Session,
    user_id: int,
    content: bytes,
    account_id: int,
    category_id: int,
    encoding: str = "utf-8",
) -> tuple[int, list[str]]:
    """Import CSV; return (created_count, list of errors)."""
    errors = []
    count = 0
    try:
        text = content.decode(encoding)
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text))
    for i, row in enumerate(reader):
        parsed = parse_row(row, user_id, account_id, category_id)
        if isinstance(parsed, str):
            errors.append(f"Row {i + 2}: {parsed}")
            continue
        session.add(Transaction(**parsed))
        count += 1
    if count:
        session.commit()
    return count, errors
