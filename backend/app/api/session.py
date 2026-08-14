from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from app.services.session_service import session_service

router = APIRouter()


class ResetRequest(BaseModel):
    session_id: str


@router.post("/reset")
def reset_session(req: ResetRequest):
    try:
        session_service.reset(req.session_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
