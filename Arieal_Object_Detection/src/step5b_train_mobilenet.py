import os
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from sklearn.metrics import classification_report, f1_score

print("\n========== STEP 5B: TRAINING MOBILENETV2 ==========\n")

# ==============================
# PATHS
# ==============================

BASE_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\data\classification_dataset"
TRAIN_DIR = os.path.join(BASE_PATH, "train")
VALID_DIR = os.path.join(BASE_PATH, "valid")

MODEL_SAVE_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\models"
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5   # Fewer epochs needed

# ==============================
# DATA GENERATORS
# ==============================

train_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
    rotation_range=30,
    horizontal_flip=True,
    zoom_range=0.2,
    brightness_range=[0.8,1.2]
)

valid_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

valid_generator = valid_datagen.flow_from_directory(
    VALID_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# ==============================
# BUILD MODEL
# ==============================

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall')
    ]
)

model.summary()

# ==============================
# CALLBACKS
# ==============================

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=2,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    os.path.join(MODEL_SAVE_PATH, "mobilenet_best.h5"),
    monitor='val_loss',
    save_best_only=True
)

# ==============================
# TRAINING
# ==============================

start_time = time.time()

history = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=EPOCHS,
    callbacks=[early_stop, checkpoint]
)

training_time = time.time() - start_time

print("\nTraining Time (seconds):", round(training_time,2))

# ==============================
# F1 SCORE
# ==============================

valid_generator.reset()
pred_probs = model.predict(valid_generator)
pred_labels = (pred_probs > 0.5).astype(int)

true_labels = valid_generator.classes

f1 = f1_score(true_labels, pred_labels)

print("\nValidation F1-Score:", round(f1,4))

print("\nClassification Report:\n")
print(classification_report(true_labels, pred_labels))

print("\n================================================\n")