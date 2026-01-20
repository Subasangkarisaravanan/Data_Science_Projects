# src/step15_baseline_model.py

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

print("=" * 70)
print("STEP 15: BASELINE MODEL – DECISION TREE")
print("=" * 70)

# Load data
X_train = pd.read_csv("data/X_train_smote.csv")
y_train = pd.read_csv("data/y_train_smote.csv").values.ravel()

X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv").values.ravel()

# Train baseline model
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# Evaluate
y_pred = dt.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Baseline Decision Tree Accuracy: {accuracy:.4f}")

print("=" * 70)
print("BASELINE MODEL COMPLETED SUCCESSFULLY")
print("=" * 70)