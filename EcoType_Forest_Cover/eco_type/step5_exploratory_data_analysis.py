# =====================================================
# STEP 5: EXPLORATORY DATA ANALYSIS (EDA)
# VISUAL STUDIO READY
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

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
# PART 1: UNIVARIATE ANALYSIS
# -----------------------------------------------------

print("Performing Univariate Analysis...")
print("-" * 60)

# Histogram for a key feature
plt.figure()
plt.hist(X["Elevation"], bins=30)
plt.title("Distribution of Elevation")
plt.xlabel("Elevation")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Boxplot for the same feature
plt.figure()
plt.boxplot(X["Elevation"])
plt.title("Boxplot of Elevation")
plt.ylabel("Elevation")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# PART 2: CLASS IMBALANCE VISUALIZATION
# -----------------------------------------------------

print("Visualizing class imbalance...")
print("-" * 60)

plt.figure()
y.value_counts().sort_index().plot(kind="bar")
plt.title("Class Distribution (Cover_Type)")
plt.xlabel("Cover Type (Encoded)")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# PART 3: BIVARIATE ANALYSIS
# -----------------------------------------------------

print("Performing Bivariate Analysis...")
print("-" * 60)

# Elevation vs Target
plt.figure(figsize=(10, 5))
sns.boxplot(x=y, y=X["Elevation"])
plt.title("Elevation vs Cover Type")
plt.xlabel("Cover Type")
plt.ylabel("Elevation")
plt.tight_layout()
plt.show()

# Scatter plot between two numeric features
plt.figure()
plt.scatter(
    X["Horizontal_Distance_To_Roadways"],
    X["Horizontal_Distance_To_Hydrology"],
    alpha=0.3
)
plt.xlabel("Distance to Roadways")
plt.ylabel("Distance to Hydrology")
plt.title("Roadways vs Hydrology Distance")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# PART 4: CORRELATION HEATMAP
# -----------------------------------------------------

print("Generating correlation heatmap...")
print("-" * 60)

corr = X.corr()

plt.figure(figsize=(12, 8))
sns.heatmap(
    corr,
    cmap="coolwarm",
    center=0
)
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# PART 5: BASELINE MODEL & FEATURE IMPORTANCE
# -----------------------------------------------------

print("Training baseline Random Forest for feature importance...")
print("-" * 60)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------------------------------
# HANDLE INF / NAN VALUES (CRITICAL)
# -----------------------------------------------------

X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_test = X_test.replace([np.inf, -np.inf], np.nan)

imputer = SimpleImputer(strategy="median")
X_train[:] = imputer.fit_transform(X_train)
X_test[:] = imputer.transform(X_test)

# -----------------------------------------------------
# TRAIN BASELINE RANDOM FOREST
# -----------------------------------------------------

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

print("Baseline Random Forest trained successfully")
print("-" * 60)

# -----------------------------------------------------
# FEATURE IMPORTANCE VISUALIZATION
# -----------------------------------------------------

feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Top 15 Important Features:")
print(feature_importance_df.head(15))
print("-" * 60)

plt.figure(figsize=(10, 6))
plt.barh(
    feature_importance_df["Feature"][:15],
    feature_importance_df["Importance"][:15]
)
plt.gca().invert_yaxis()
plt.xlabel("Importance")
plt.title("Top 15 Feature Importances (Random Forest)")
plt.tight_layout()
plt.show()

print("✅ STEP 5: EXPLORATORY DATA ANALYSIS COMPLETED SUCCESSFULLY")