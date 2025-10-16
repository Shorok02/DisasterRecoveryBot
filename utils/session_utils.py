# utils/session_utils.py

from datetime import datetime
from db.database import get_user_by_telegram_id


def is_session_active(telegram_id):
    row = get_user_by_telegram_id(telegram_id)
    if not row:
        return False
    expiry = datetime.fromisoformat(row[0])
    return datetime.now() < expiry
