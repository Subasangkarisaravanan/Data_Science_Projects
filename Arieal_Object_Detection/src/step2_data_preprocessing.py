import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess

# ==============================
# PATHS
# ==============================

BASE_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\data\classification_dataset"

TRAIN_DIR = os.path.join(BASE_PATH, "train")
VALID_DIR = os.path.join(BASE_PATH, "valid")
TEST_DIR = os.path.join(BASE_PATH, "test")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32


# ==============================
# 1️⃣ NORMALIZATION TO [0,1]
# ==============================

print("\n===== BASIC NORMALIZATION (0–1) =====\n")

basic_datagen = ImageDataGenerator(rescale=1./255)

train_generator_basic = basic_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Get one batch
images, labels = next(train_generator_basic)

print("Image batch shape:", images.shape)
print("Image dtype:", images.dtype)
print("Min pixel value:", images.min())
print("Max pixel value:", images.max())
print("Labels shape:", labels.shape)

print("\n=====================================\n")


# ==============================
# 2️⃣ TRANSFER LEARNING PREPROCESSING
# ==============================

print("===== TRANSFER LEARNING PREPROCESSING =====\n")

resnet_datagen = ImageDataGenerator(preprocessing_function=resnet_preprocess)

resnet_generator = resnet_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

resnet_images, _ = next(resnet_generator)

print("ResNet Preprocessed Image Min:", resnet_images.min())
print("ResNet Preprocessed Image Max:", resnet_images.max())

print("\n==========================================\n")


# ==============================
# 3️⃣ VISUALIZE BEFORE & AFTER
# ==============================

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(images[0])
plt.title("Normalized [0,1]")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow((resnet_images[0] - resnet_images[0].min()) /
           (resnet_images[0].max() - resnet_images[0].min()))
plt.title("ResNet Preprocessed")
plt.axis("off")

plt.tight_layout()
plt.show()


# ==============================
# 4️⃣ PYTORCH NORMALIZATION (REFERENCE ONLY)
# ==============================

print("\n===== PYTORCH NORMALIZATION REFERENCE =====\n")

print("""
For PyTorch pretrained models, use:

transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

This is ImageNet normalization as required in the project document.
""")

print("=============================================\n")