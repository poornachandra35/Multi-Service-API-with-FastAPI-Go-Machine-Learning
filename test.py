import numpy as np
import tensorflow as tf
import os

# -------------------------
# SETTINGS
# -------------------------
SAVE_DIR = "modules/stock_predictor/model"
SEQ_LEN = 5

os.makedirs(SAVE_DIR, exist_ok=True)

# -------------------------
# 1. GENERATE SYNTHETIC STOCK DATA (LIKE REAL MARKET)
# -------------------------
print("Generating synthetic stock data...")

np.random.seed(42)

days = 1000  # number of data points (you can increase this)
base_price = 1500

# Random walk + slight upward trend + noise
noise = np.random.normal(0, 8, days)
trend = np.linspace(0, 200, days)       # trend over time
walk = np.cumsum(np.random.normal(0, 3, days))

prices = base_price + trend + walk + noise

prices = prices.astype(float)

print("Total synthetic prices:", len(prices))

# -------------------------
# 2. CREATE DATASET
# -------------------------
X, y = [], []

for i in range(len(prices) - SEQ_LEN):
    X.append(prices[i:i+SEQ_LEN])
    y.append(prices[i+SEQ_LEN])

X = np.array(X)
y = np.array(y)

print("Dataset created:", X.shape, y.shape)

# -------------------------
# 3. NORMALIZATION
# -------------------------
min_val = X.min()
max_val = X.max()

np.save(f"{SAVE_DIR}/min.npy", min_val)
np.save(f"{SAVE_DIR}/max.npy", max_val)

X_norm = (X - min_val) / (max_val - min_val)
y_norm = (y - min_val) / (max_val - min_val)

# -------------------------
# 4. BUILD ANN MODEL
# -------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(SEQ_LEN,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')

print(model.summary())

# -------------------------
# 5. TRAIN
# -------------------------
print("Training model...")
model.fit(X_norm, y_norm, epochs=80, batch_size=32, verbose=1)

# -------------------------
# 6. SAVE MODEL
# -------------------------
model.save(f"{SAVE_DIR}/stock_ann.h5")
print("\nModel saved successfully!")

print("\nGenerated files:")
print("- stock_ann.h5")
print("- min.npy")
print("- max.npy")
