# =====================================================
# STEP 6: CLASS IMBALANCE HANDLING (SMOTE)
# VISUAL STUDIO READY
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

# -----------------------------------------------------
# LOAD FEATURE-ENGINEERED DATASET
# -----------------------------------------------------

DATA_PATH = "data/cover_type_feature_engineered.csv"

df = pd.read_csv(DATA_PATH)

print("Feature-engineered dataset loaded")
print("Dataset shape:", df.shape)
print("-" * 60)

# -----------------------------------------------------
# SEPARATE FEATURES & TARGET
# -----------------------------------------------------

X = df.drop("Cover_Type", axis=1)
y = df["Cover_Type"]

# -----------------------------------------------------
# TRAIN / TEST SPLIT (VERY IMPORTANT)
# -----------------------------------------------------
# SMOTE MUST be applied ONLY on training data

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
# CHECK CLASS DISTRIBUTION (BEFORE SMOTE)
# -----------------------------------------------------

print("Class distribution BEFORE SMOTE:")
print(y_train.value_counts())
print("-" * 60)

plt.figure()
y_train.value_counts().sort_index().plot(kind="bar")
plt.title("Class Distribution BEFORE SMOTE")
plt.xlabel("Class")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# HANDLE INF & NaN VALUES (CRITICAL FOR SMOTE)
# -----------------------------------------------------

X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_test  = X_test.replace([np.inf, -np.inf], np.nan)

imputer = SimpleImputer(strategy="median")

X_train = pd.DataFrame(
    imputer.fit_transform(X_train),
    columns=X_train.columns
)

X_test = pd.DataFrame(
    imputer.transform(X_test),
    columns=X_test.columns
)

print("Missing and infinite values handled using median imputation")
print("-" * 60)

# -----------------------------------------------------
# APPLY SMOTE (ONLY ON TRAINING DATA)
# -----------------------------------------------------

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("SMOTE applied successfully")
print("-" * 60)

# -----------------------------------------------------
# CHECK CLASS DISTRIBUTION (AFTER SMOTE)
# -----------------------------------------------------

print("Class distribution AFTER SMOTE:")
print(y_train_smote.value_counts())
print("-" * 60)

plt.figure()
y_train_smote.value_counts().sort_index().plot(kind="bar")
plt.title("Class Distribution AFTER SMOTE")
plt.xlabel("Class")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# FINAL DATA TO USE FOR MODEL TRAINING
# -----------------------------------------------------

X_train_final = X_train_smote
y_train_final = y_train_smote

print("Final training data prepared")
print("X_train_final shape:", X_train_final.shape)
print("y_train_final shape:", y_train_final.shape)
print("-" * 60)

print("✅ STEP 6: CLASS IMBALANCE HANDLING COMPLETED SUCCESSFULLY")