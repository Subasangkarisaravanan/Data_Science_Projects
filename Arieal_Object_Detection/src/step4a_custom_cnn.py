import tensorflow as tf
from tensorflow.keras import layers, models

print("\n========== STEP 4A: CUSTOM CNN MODEL ==========\n")

IMG_SHAPE = (224, 224, 3)

# =====================================================
# BUILD MODEL
# =====================================================

model = models.Sequential([

    layers.Input(shape=IMG_SHAPE),

    # Block 1
    layers.Conv2D(32, (3,3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Block 2
    layers.Conv2D(64, (3,3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Block 3
    layers.Conv2D(128, (3,3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Block 4
    layers.Conv2D(256, (3,3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Fully Connected
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')   # Binary classification

])

# =====================================================
# COMPILE MODEL
# =====================================================

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# =====================================================
# PRINT MODEL DETAILS
# =====================================================

model.summary()

print("\nTotal Trainable Parameters:", model.count_params())

print("\n===============================================\n")