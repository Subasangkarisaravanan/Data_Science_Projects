import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

print("=" * 70)
print("STEP 18: HYPERPARAMETER TUNING")
print("=" * 70)

X_train = pd.read_csv("data/X_train_smote.csv")
y_train = pd.read_csv("data/y_train_smote.csv").values.ravel()

param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 20, 30]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring="accuracy",
    n_jobs=-1
)

grid.fit(X_train, y_train)

print("Best Parameters:", grid.best_params_)
print("Best CV Accuracy:", round(grid.best_score_, 4))

print("=" * 70)