import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers

# ==============================
# PATH CONFIGURATION
# ==============================

BASE_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\data\classification_dataset"

TRAIN_DIR = os.path.join(BASE_PATH, "train")
VALID_DIR = os.path.join(BASE_PATH, "valid")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

print("\n========== STEP 3: DATA AUGMENTATION ==========\n")

# =====================================================
# 1️⃣ TRAIN DATA AUGMENTATION (INCLUDING CROPPING)
# =====================================================

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,                # Rotation
    horizontal_flip=True,             # Flipping
    zoom_range=0.2,                   # Zoom
    brightness_range=[0.8, 1.2],      # Brightness
)

# Validation set: NO augmentation (as required)
valid_datagen = ImageDataGenerator(rescale=1./255)

# Generators
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=True
)

valid_generator = valid_datagen.flow_from_directory(
    VALID_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# =====================================================
# 2️⃣ APPLY CROPPING USING KERAS RANDOM-CROP
# =====================================================

random_crop_layer = layers.RandomCrop(200, 200)

# Get one batch
images, labels = next(train_generator)

# Apply cropping
cropped_images = random_crop_layer(images)

# Resize back to 224x224 after cropping
resized_images = tf.image.resize(cropped_images, IMG_SIZE)

# =====================================================
# 3️⃣ PRINT DETAILED OUTPUTS
# =====================================================

print("Train Images Found:", train_generator.samples)
print("Validation Images Found:", valid_generator.samples)

print("\nAugmentation Applied:")
print("- Rotation: 30 degrees")
print("- Horizontal Flip: Enabled")
print("- Zoom Range: 0.2")
print("- Brightness Range: [0.8, 1.2]")
print("- Random Cropping: 200x200 -> Resized to 224x224")

print("\nBatch Shape (After Augmentation):", resized_images.shape)
print("Data Type:", resized_images.dtype)
print("Min Pixel Value:", tf.reduce_min(resized_images).numpy())
print("Max Pixel Value:", tf.reduce_max(resized_images).numpy())

print("\n===============================================\n")

# =====================================================
# 4️⃣ VISUALIZE AUGMENTED IMAGES
# =====================================================

print("Displaying Augmented & Cropped Samples...\n")

plt.figure(figsize=(8, 8))

for i in range(9):
    plt.subplot(3, 3, i+1)
    plt.imshow(resized_images[i])
    plt.axis("off")

plt.tight_layout()
plt.show()