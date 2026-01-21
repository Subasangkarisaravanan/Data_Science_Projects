# =====================================================
# STEP 8: MODEL BUILDING & EVALUATION
# VISUAL STUDIO READY
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from xgboost import XGBClassifier

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
# FEATURE SCALING (FOR LR & KNN)
# -----------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------------------------------
# MODEL EVALUATION FUNCTION
# -----------------------------------------------------

def evaluate_model(model, X_tr, X_te, y_tr, y_te, model_name):
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)

    print(f"\n===== {model_name} =====")
    print("Accuracy:", accuracy_score(y_te, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_te, y_pred))

    cm = confusion_matrix(y_te, y_pred)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=False, cmap="Blues")
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()

# -----------------------------------------------------
# 1️⃣ RANDOM FOREST
# -----------------------------------------------------

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

evaluate_model(rf, X_train, X_test, y_train, y_test, "Random Forest")

# -----------------------------------------------------
# 2️⃣ DECISION TREE
# -----------------------------------------------------

dt = DecisionTreeClassifier(
    random_state=42
)

evaluate_model(dt, X_train, X_test, y_train, y_test, "Decision Tree")

# -----------------------------------------------------
# 3️⃣ LOGISTIC REGRESSION
# -----------------------------------------------------

lr = LogisticRegression(
    max_iter=1000,
    n_jobs=-1
)

evaluate_model(
    lr,
    X_train_scaled,
    X_test_scaled,
    y_train,
    y_test,
    "Logistic Regression"
)

# -----------------------------------------------------
# 4️⃣ K-NEAREST NEIGHBORS (KNN)
# -----------------------------------------------------

knn = KNeighborsClassifier(
    n_neighbors=5
)

evaluate_model(
    knn,
    X_train_scaled,
    X_test_scaled,
    y_train,
    y_test,
    "KNN"
)

# -----------------------------------------------------
# 5️⃣ XGBOOST
# -----------------------------------------------------

xgb = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    objective="multi:softmax",
    num_class=len(y.unique()),
    eval_metric="mlogloss",
    random_state=42
)

evaluate_model(xgb, X_train, X_test, y_train, y_test, "XGBoost")

print("\n✅ STEP 8: MODEL BUILDING & EVALUATION COMPLETED SUCCESSFULLY")