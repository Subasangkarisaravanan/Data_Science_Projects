import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report

print("\n========== STEP 6: MODEL EVALUATION ==========\n")

# ==============================
# PATHS
# ==============================

BASE_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\data\classification_dataset"
TEST_DIR = os.path.join(BASE_PATH, "test")

MODEL_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\models\mobilenet_best.h5"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ==============================
# LOAD MODEL
# ==============================

model = tf.keras.models.load_model(MODEL_PATH)

print("Model Loaded Successfully.\n")

# ==============================
# TEST DATA GENERATOR
# ==============================

test_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# ==============================
# PREDICTIONS
# ==============================

pred_probs = model.predict(test_generator)
pred_labels = (pred_probs > 0.5).astype(int)

true_labels = test_generator.classes

# ==============================
# CONFUSION MATRIX
# ==============================

cm = confusion_matrix(true_labels, pred_labels)

print("Confusion Matrix:\n")
print(cm)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=['Bird','Drone'],
            yticklabels=['Bird','Drone'],
            cmap='Blues')

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# ==============================
# CLASSIFICATION REPORT
# ==============================

print("\nClassification Report (TEST SET):\n")
print(classification_report(true_labels, pred_labels))

print("\n=============================================\n")