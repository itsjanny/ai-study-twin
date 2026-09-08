import json
import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import Request
from app.models.db_models import UserActivityLog, UserSession

class AuditService:
    @staticmethod
    def log_activity(
        db: Session,
        action_type: str,
        user_id: Optional[int] = None,
        endpoint: Optional[str] = None,
        request: Optional[Request] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> UserActivityLog:
        ip_addr = "127.0.0.1"
        user_agent_str = "Unknown"

        if request:
            if request.client:
                ip_addr = request.client.host
            user_agent_str = request.headers.get("user-agent", "Unknown")
            if not endpoint:
                endpoint = str(request.url.path)

        log_entry = UserActivityLog(
            user_id=user_id,
            action_type=action_type,
            endpoint=endpoint,
            ip_address=ip_addr,
            user_agent=user_agent_str[:500] if user_agent_str else None,
            details_json=json.dumps(details) if details else None,
            created_at=datetime.datetime.utcnow()
        )

        try:
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
        except Exception as e:
            db.rollback()
            print(f"Audit log failed: {e}")

        return log_entry

audit_service = AuditService()
