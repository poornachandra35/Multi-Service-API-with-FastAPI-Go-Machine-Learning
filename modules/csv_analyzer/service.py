import io, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from modules.csv_analyzer.session_store import get_session_df, make_session

# ---------- Upload ----------
async def handle_upload(file, sheet=None):
    contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            xls = pd.ExcelFile(io.BytesIO(contents))
            df = pd.read_excel(io.BytesIO(contents), sheet_name=sheet or xls.sheet_names[0])
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    sid = make_session(df)
    return {"session_id": sid, "rows": len(df), "cols": len(df.columns), "columns": list(df.columns)}

# ---------- Preview ----------
def get_preview(session_id: str, n: int, tail: bool):
    df = get_session_df(session_id)
    data = df.tail(n) if tail else df.head(n)
    return {"rows": len(data), "data": data.to_dict(orient="records")}

# ---------- Summary ----------
def get_summary(session_id: str):
    df = get_session_df(session_id)
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isna().sum().to_dict()
    }

# ---------- Plot Histogram ----------
def plot_histogram(session_id: str, column: str):
    df = get_session_df(session_id)
    if column not in df.columns:
        raise HTTPException(status_code=400, detail="Column not found")
    if not np.issubdtype(df[column].dtype, np.number):
        raise HTTPException(status_code=400, detail="Column must be numeric")

    fig = plt.figure()
    sns.histplot(df[column].dropna(), kde=True)
    plt.title(f"Histogram of {column}")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# ---------- Drop Duplicates ----------
def drop_duplicates(session_id: str, subset: str = None):
    df = get_session_df(session_id)
    cleaned = df.copy()
    if subset:
        cols = [c.strip() for c in subset.split(',')]
        invalid = [c for c in cols if c not in df.columns]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid columns: {invalid}")
        cleaned = cleaned.drop_duplicates(subset=cols)
    else:
        cleaned = cleaned.drop_duplicates()
    make_session(cleaned)
    return {"status": "ok", "rows": len(cleaned), "cols": len(cleaned.columns)}
