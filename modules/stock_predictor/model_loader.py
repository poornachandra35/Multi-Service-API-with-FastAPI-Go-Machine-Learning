import numpy as np
import tensorflow as tf

class StockANNModel:
    def __init__(self):
        self.model = tf.keras.models.load_model(
    "modules/stock_predictor/model/stock_ann.h5",
    compile=False
)


        # Load scaling values
        self.min = np.load("modules/stock_predictor/model/min.npy")
        self.max = np.load("modules/stock_predictor/model/max.npy")

    def normalize(self, prices):
        return (np.array(prices) - self.min) / (self.max - self.min)

    def denormalize(self, value):
        return value * (self.max - self.min) + self.min

    def predict_next(self, prices):
        norm = self.normalize(prices)
        norm = norm.reshape(1, -1)
        pred = self.model.predict(norm)[0][0]

        return float(self.denormalize(pred))


stock_ann = StockANNModel()
