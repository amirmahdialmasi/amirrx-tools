import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =========================
# Settings
# =========================

DATASET_FILE = "dataset.csv"
MODEL_FILE = "compression_model.pkl"


FEATURES = [
    "width",
    "height",
    "original_size",
    "brightness",
    "contrast",
    "color_variance",
    "edge_density",
    "entropy"
]

TARGET = "recommended_quality"


# =========================
# Load Dataset
# =========================

df = pd.read_csv(
    DATASET_FILE
)


# =========================
# Remove Invalid Rows
# =========================

df = df.dropna(
    subset=FEATURES + [TARGET]
)


# =========================
# Features / Target
# =========================

X = df[FEATURES]

y = df[TARGET]


# =========================
# Train / Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================
# Create Model
# =========================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)


# =========================
# Train
# =========================

model.fit(
    X_train,
    y_train
)


# =========================
# Test
# =========================

predictions = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print(
    "===== Smart Compression Model ====="
)

print(
    f"MAE: {mae:.2f}"
)

print(
    f"R²: {r2:.4f}"
)


# =========================
# Feature Importance
# =========================

print()
print(
    "===== Feature Importance ====="
)

importance = model.feature_importances_

for feature, value in sorted(
    zip(FEATURES, importance),
    key=lambda item: item[1],
    reverse=True
):

    print(
        f"{feature}: {value:.4f}"
    )


# =========================
# Save Model
# =========================

joblib.dump(
    model,
    MODEL_FILE
)


print()
print(
    f"Model saved to: {MODEL_FILE}"
)