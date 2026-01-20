import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

print("=" * 70)
print("STEP 17: XGBOOST MODEL")
print("=" * 70)

X_train = pd.read_csv("data/X_train_smote.csv")
y_train = pd.read_csv("data/y_train_smote.csv").values.ravel()

X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv").values.ravel()

model = XGBClassifier(
    objective="multi:softmax",
    num_class=7,
    eval_metric="mlogloss",
    random_state=42
)

model.fit(X_train, y_train)
preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
print(f"XGBoost Accuracy: {acc:.4f}")

print("=" * 70)