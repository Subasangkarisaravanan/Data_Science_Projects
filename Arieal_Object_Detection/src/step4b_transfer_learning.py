import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50, MobileNetV2, EfficientNetB0

print("\n========== STEP 4B: TRANSFER LEARNING ==========\n")

IMG_SHAPE = (224, 224, 3)

# =====================================================
# FUNCTION TO BUILD TRANSFER MODEL
# =====================================================

def build_transfer_model(base_model_class, model_name):
    print(f"\n--- Building {model_name} ---\n")

    base_model = base_model_class(
        weights='imagenet',
        include_top=False,
        input_shape=IMG_SHAPE
    )

    base_model.trainable = False  # Freeze base model

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
        metrics=['accuracy']
    )

    model.summary()

    print("\nTotal Parameters:", model.count_params())
    print("Trainable Parameters:",
          sum([tf.keras.backend.count_params(w)
               for w in model.trainable_weights]))
    print("Non-Trainable Parameters:",
          sum([tf.keras.backend.count_params(w)
               for w in model.non_trainable_weights]))

    print("\n---------------------------------------------\n")

    return model


# =====================================================
# BUILD ALL REQUIRED MODELS
# =====================================================

resnet_model = build_transfer_model(ResNet50, "ResNet50")
mobilenet_model = build_transfer_model(MobileNetV2, "MobileNetV2")
efficientnet_model = build_transfer_model(EfficientNetB0, "EfficientNetB0")

print("\n========== TRANSFER MODELS BUILT SUCCESSFULLY ==========\n")