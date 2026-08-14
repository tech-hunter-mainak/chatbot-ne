import json
from pathlib import Path
from typing import Optional

_BASE = Path(__file__).resolve().parents[2] / "memories" / "session"


class SessionService:
    def __init__(self):
        self._base = _BASE
        self._base.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        safe = "_".join(ch for ch in session_id if ch.isalnum() or ch in "-_") or "anon"
        return self._base / f"{safe}.json"

    def append(self, session_id: str, entry: dict):
        p = self._path(session_id)
        data = []
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                data = []
        data.append(entry)
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def get(self, session_id: str) -> list:
        p = self._path(session_id)
        if not p.exists():
            return []
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return []

    def reset(self, session_id: str):
        p = self._path(session_id)
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass


session_service = SessionService()
