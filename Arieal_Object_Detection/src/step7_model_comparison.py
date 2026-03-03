print("\n========== STEP 7: MODEL COMPARISON ==========\n")

# Manually entering recorded metrics from previous steps

models = {
    "Custom CNN": {
        "Validation Accuracy": 0.44,
        "Validation F1": 0.52,
        "Training Time (sec)": 1086
    },
    "MobileNetV2": {
        "Validation Accuracy": 0.98,
        "Validation F1": 0.9755,
        "Training Time (sec)": 526
    }
}

print("Model Comparison:\n")

for model_name, metrics in models.items():
    print(f"--- {model_name} ---")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
    print()

print("Best Performing Model: MobileNetV2")
print("Reason: Highest Accuracy, Highest F1, Lower Training Time")

print("\nSaving MobileNet as Final Deployment Model...\n")