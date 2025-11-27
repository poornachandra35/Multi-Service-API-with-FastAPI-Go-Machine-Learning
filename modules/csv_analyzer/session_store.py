import uuid
from fastapi import HTTPException

SESSIONS = {}

def make_session(df):
    sid = str(uuid.uuid4())
    SESSIONS[sid] = {"df": df.copy(), "cleaned": df.copy()}
    return sid

def get_session_df(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    return SESSIONS[session_id]["cleaned"]
