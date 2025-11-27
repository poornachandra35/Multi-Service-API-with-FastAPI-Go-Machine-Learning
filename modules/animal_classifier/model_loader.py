import tensorflow as tf
import numpy as np
from PIL import Image
from .labels_map import ANIMAL_MAP

class MultiAnimalModel:
    def __init__(self):
        self.model = tf.keras.applications.MobileNetV2(
            weights="imagenet"
        )

    def predict(self, img):
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        preds = self.model.predict(img_array)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        results = []
        for (_, label, score) in decoded:
            simple = ANIMAL_MAP.get(label, None)
            if simple:
                results.append({
                    "imagenet_label": label,
                    "simple_label": simple,
                    "confidence": float(score)
                })

        if not results:
            return {"prediction": "unknown", "confidence": 0}

        # Best prediction
        best = max(results, key=lambda x: x["confidence"])
        return best


animal_model = MultiAnimalModel()
