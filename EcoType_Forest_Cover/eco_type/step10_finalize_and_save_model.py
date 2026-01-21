# =====================================================
# STEP 10: FINALIZE AND SAVE BEST MODEL
# MODEL: RANDOM FOREST
# VISUAL STUDIO READY
# =====================================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------------------------------
# LOAD FEATURE-SELECTED DATASET
# -----------------------------------------------------

DATA_PATH = "data/cover_type_selected_features.csv"

df = pd.read_csv(DATA_PATH)

print("Feature-selected dataset loaded")
print("Dataset shape:", df.shape)
print("-" * 60)

# -----------------------------------------------------
# SEPARATE FEATURES & TARGET
# -----------------------------------------------------

X = df.drop("Cover_Type", axis=1)
y = df["Cover_Type"]

print("Features shape:", X.shape)
print("Target shape:", y.shape)
print("-" * 60)

# -----------------------------------------------------
# TRAIN / TEST SPLIT
# -----------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train/Test split completed")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("-" * 60)

# -----------------------------------------------------
# INITIALIZE FINAL RANDOM FOREST MODEL
# (Best hyperparameters from Step 9 tuning)
# -----------------------------------------------------

final_rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=30,
    max_features="log2",
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

# -----------------------------------------------------
# TRAIN FINAL MODEL
# -----------------------------------------------------

final_rf.fit(X_train, y_train)

print("Final Random Forest model trained successfully")
print("-" * 60)

# -----------------------------------------------------
# FINAL EVALUATION (SANITY CHECK)
# -----------------------------------------------------

y_pred = final_rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Final Model Accuracy:", accuracy)
print("-" * 60)

print("Final Classification Report:")
print(classification_report(y_test, y_pred))
print("-" * 60)

# -----------------------------------------------------
# SAVE MODEL & FEATURE LIST
# -----------------------------------------------------

MODEL_PATH = "models/final_random_forest_model.pkl"
FEATURES_PATH = "models/model_features.pkl"

joblib.dump(final_rf, MODEL_PATH)
joblib.dump(list(X.columns), FEATURES_PATH)

print("Model saved at:", MODEL_PATH)
print("Feature list saved at:", FEATURES_PATH)
print("-" * 60)

print("✅ STEP 10: FINALIZE AND SAVE BEST MODEL COMPLETED SUCCESSFULLY")