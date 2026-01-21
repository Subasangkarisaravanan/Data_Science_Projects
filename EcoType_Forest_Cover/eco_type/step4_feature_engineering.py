# =====================================================
# STEP 4: FEATURE ENGINEERING (VISUAL STUDIO READY)
# =====================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import joblib
import os

# -----------------------------------------------------
# PATHS
# -----------------------------------------------------

DATA_PATH = "data/cover_type_cleaned.csv"
OUTPUT_DATA_PATH = "data/cover_type_feature_engineered.csv"
ENCODER_DIR = "models"

os.makedirs(ENCODER_DIR, exist_ok=True)

# -----------------------------------------------------
# LOAD CLEANED DATASET
# -----------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Cleaned dataset loaded successfully")
print("Dataset shape:", df.shape)
print("-" * 50)

# -----------------------------------------------------
# IDENTIFY COLUMN TYPES
# -----------------------------------------------------

continuous_cols = [
    'Elevation',
    'Aspect',
    'Slope',
    'Horizontal_Distance_To_Hydrology',
    'Horizontal_Distance_To_Roadways',
    'Hillshade_9am',
    'Hillshade_Noon',
    'Hillshade_3pm',
    'Horizontal_Distance_To_Fire_Points'
]

categorical_cols = [
    'Wilderness_Area',
    'Soil_Type'
]

target_col = 'Cover_Type'

print("Continuous columns:", continuous_cols)
print("Categorical columns:", categorical_cols)
print("Target column:", target_col)
print("-" * 50)

# -----------------------------------------------------
# FEATURE ANALYSIS (OPTIONAL CHECK)
# -----------------------------------------------------

print("Skewness of continuous features:")
print(df[continuous_cols].skew())
print("-" * 50)

# -----------------------------------------------------
# DERIVED / INTERACTION FEATURES
# -----------------------------------------------------

df['Hydrology_Road_Ratio'] = (
    df['Horizontal_Distance_To_Hydrology'] /
    (df['Horizontal_Distance_To_Roadways'] + 1)
)

df['Fire_Road_Ratio'] = (
    df['Horizontal_Distance_To_Fire_Points'] /
    (df['Horizontal_Distance_To_Roadways'] + 1)
)

df['Hillshade_Diff'] = (
    df['Hillshade_Noon'] - df['Hillshade_9am']
)

print("Derived features created:")
print([
    'Hydrology_Road_Ratio',
    'Fire_Road_Ratio',
    'Hillshade_Diff'
])
print("-" * 50)

# -----------------------------------------------------
# SEPARATE FEATURES & TARGET
# -----------------------------------------------------

X = df.drop(target_col, axis=1)
y = df[target_col]

# -----------------------------------------------------
# ENCODE CATEGORICAL FEATURES
# -----------------------------------------------------

feature_encoder = OneHotEncoder(
    sparse_output=False,
    handle_unknown='ignore'
)

encoded_cat = feature_encoder.fit_transform(X[categorical_cols])

encoded_cat_df = pd.DataFrame(
    encoded_cat,
    columns=feature_encoder.get_feature_names_out(categorical_cols)
)

X_final = pd.concat(
    [
        X.drop(categorical_cols, axis=1).reset_index(drop=True),
        encoded_cat_df.reset_index(drop=True)
    ],
    axis=1
)

print("Categorical features encoded successfully")
print("Final feature shape:", X_final.shape)
print("-" * 50)

# -----------------------------------------------------
# ENCODE TARGET VARIABLE
# -----------------------------------------------------

target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

print("Target variable encoded")
print("Target classes:", list(target_encoder.classes_))
print("-" * 50)

# -----------------------------------------------------
# SAVE ENCODERS (CRITICAL FOR INFERENCE)
# -----------------------------------------------------

joblib.dump(feature_encoder, os.path.join(ENCODER_DIR, "feature_encoder.joblib"))
joblib.dump(target_encoder, os.path.join(ENCODER_DIR, "target_encoder.joblib"))

print("Encoders saved successfully in 'models/'")
print("-" * 50)

# -----------------------------------------------------
# SAVE FEATURE-ENGINEERED DATASET
# -----------------------------------------------------

X_final['Cover_Type'] = y_encoded

X_final.to_csv(OUTPUT_DATA_PATH, index=False)

print("Feature-engineered dataset saved at:")
print(OUTPUT_DATA_PATH)
print("-" * 50)

print("✅ STEP 4: FEATURE ENGINEERING COMPLETED SUCCESSFULLY")