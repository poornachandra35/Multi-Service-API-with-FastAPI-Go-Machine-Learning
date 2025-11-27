from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/api-guide", include_in_schema=False)
def api_guide(request: Request):

    # Access app WITHOUT importing main.py → no circular import
    app = request.app

    routes_info = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.path not in ["/docs", "/redoc"]:
                routes_info.append({
                    "path": route.path,
                    "methods": list(route.methods - {"HEAD", "OPTIONS"}),
                    "summary": route.summary or "",
                    "tags": route.tags or []
                })

    overview = {
        "description": "Central guide describing how to use every module.",
        "modules": [
            {"name": "CSV Analyzer", "prefix": "/csv"},
            {"name": "Sentiment Analyzer", "prefix": "/sentiment"},
            {"name": "Number Series Predictor", "prefix": "/series"},
        ]
    }

    return templates.TemplateResponse(
        "api_guide.html",
        {
            "request": request,
            "overview": overview,
            "routes": routes_info
        }
    )
