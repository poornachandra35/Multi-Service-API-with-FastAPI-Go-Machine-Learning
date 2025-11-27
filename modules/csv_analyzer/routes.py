from fastapi import APIRouter, UploadFile, File, Form
from modules.csv_analyzer import service

router = APIRouter()

# File Upload
@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), sheet: str = Form(None)):
    return await service.handle_upload(file, sheet)

# Preview
@router.get("/preview/{session_id}")
def preview(session_id: str, n: int = 5, tail: bool = False):
    return service.get_preview(session_id, n, tail)

# Summary
@router.get("/summary/{session_id}")
def summary(session_id: str):
    return service.get_summary(session_id)

# Histogram Plot
@router.get("/plot/hist/{session_id}")
def plot_hist(session_id: str, column: str):
    return service.plot_histogram(session_id, column)

# Drop Duplicates
@router.post("/clean/drop_duplicates/{session_id}")
def drop_duplicates(session_id: str, subset: str = Form(None)):
    return service.drop_duplicates(session_id, subset)
