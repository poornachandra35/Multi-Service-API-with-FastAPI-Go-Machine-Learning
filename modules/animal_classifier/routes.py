from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from .model_loader import animal_model

router = APIRouter(
    prefix="/animal",
    tags=["Multi-Animal Classifier (MobileNetV2 CNN)"]
)

@router.post("/predict")
async def predict_animal(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(("png", "jpg", "jpeg")):
        raise HTTPException(status_code=400, detail="Only images allowed")

    img = Image.open(file.file).convert("RGB")

    result = animal_model.predict(img)

    return {
        "prediction": result["simple_label"],
        "imagenet_label": result["imagenet_label"],
        "confidence": result["confidence"]
    }
