# =====================================================
# STEP 9: HYPERPARAMETER TUNING
# MODEL: RANDOM FOREST
# METHOD: RANDOMIZEDSEARCHCV
# VISUAL STUDIO READY
# =====================================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, RandomizedSearchCV
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

# -----------------------------------------------------
# TRAIN / TEST SPLIT
# -----------------------------------------------------
# IMPORTANT: Hyperparameter tuning must use ONLY training data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train/Test split completed")
print("Training shape:", X_train.shape)
print("Testing shape:", X_test.shape)
print("-" * 60)

# -----------------------------------------------------
# BASE RANDOM FOREST MODEL
# -----------------------------------------------------

rf = RandomForestClassifier(
    random_state=42,
    n_jobs=-1
)

# -----------------------------------------------------
# HYPERPARAMETER SEARCH SPACE
# -----------------------------------------------------

param_distributions = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"]
}

# -----------------------------------------------------
# RANDOMIZED SEARCH SETUP
# -----------------------------------------------------

rf_random = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_distributions,
    n_iter=20,
    cv=3,
    scoring="accuracy",
    random_state=42,
    n_jobs=-1,
    verbose=2
)

print("Starting hyperparameter tuning using RandomizedSearchCV...")
print("-" * 60)

# -----------------------------------------------------
# RUN HYPERPARAMETER TUNING
# -----------------------------------------------------

rf_random.fit(X_train, y_train)

print("-" * 60)
print("Hyperparameter tuning completed")

# -----------------------------------------------------
# BEST PARAMETERS
# -----------------------------------------------------

print("Best hyperparameters found:")
print(rf_random.best_params_)
print("-" * 60)

# -----------------------------------------------------
# TRAIN FINAL MODEL WITH BEST PARAMETERS
# -----------------------------------------------------

best_rf = rf_random.best_estimator_

# -----------------------------------------------------
# EVALUATE TUNED MODEL ON TEST SET
# -----------------------------------------------------

y_pred = best_rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Tuned Random Forest Accuracy:", accuracy)
print("-" * 60)

print("Classification Report (Tuned Random Forest):")
print(classification_report(y_test, y_pred))
print("-" * 60)

print("✅ STEP 9: HYPERPARAMETER TUNING COMPLETED SUCCESSFULLY")