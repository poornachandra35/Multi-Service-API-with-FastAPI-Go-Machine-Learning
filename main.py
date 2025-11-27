from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import module routers
from modules.csv_analyzer.routes import router as csv_router
from modules.sentiment_analyzer.routes import router as sentiment_router
from modules.series_analyzer.routes import router as series_router
from guides.api_guide import router as guide_router
from modules.animal_classifier.routes import router as animal_router
from modules.stock_predictor.routes import router as stock_router







# from app.modules.qr_generator.routes import router as qr_router  # for future use

app = FastAPI(title="API Service Platform", version="1.0")

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(guide_router)
app.include_router(animal_router)
app.include_router(stock_router)
app.include_router(sentiment_router)
app.include_router(csv_router, prefix="/csv", tags=["CSV Analyzer"])
app.include_router(series_router, prefix="/series", tags=["Number Series Predictor"])




# app.include_router(qr_router, prefix="/qr", tags=["QR Generator"])

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Service API Platform 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
