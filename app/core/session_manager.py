# app/core/session_manager.py
import time
from typing import Dict

class SessionManager:
    def __init__(self):
        # phone -> expiry_ts
        self.sessions: Dict[str, float] = {}

    def create_session(self, phone: str, duration_seconds: int = 3600):
        self.sessions[phone] = time.time() + duration_seconds

    def is_active(self, phone: str) -> bool:
        expiry = self.sessions.get(phone)
        if not expiry:
            return False
        if time.time() > expiry:
            # cleanup expired
            self.sessions.pop(phone, None)
            return False
        return True

    def end_session(self, phone: str):
        self.sessions.pop(phone, None)
