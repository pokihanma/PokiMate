"""Append-only audit log for mutations."""
from sqlmodel import Session
from app.models.audit_event import AuditEvent
import json


def log_event(
    session: Session,
    user_id: int,
    actor_user_id: int | None,
    device_id: str | None,
    event_type: str,
    entity: str,
    entity_id: int | None,
    old_value: dict | None,
    new_value: dict | None,
) -> None:
    old_json = json.dumps(old_value) if old_value is not None else None
    new_json = json.dumps(new_value) if new_value is not None else None
    event = AuditEvent(
        user_id=user_id,
        actor_user_id=actor_user_id,
        device_id=device_id,
        event_type=event_type,
        entity=entity,
        entity_id=entity_id,
        old_json=old_json,
        new_json=new_json,
    )
    session.add(event)
    session.commit()
