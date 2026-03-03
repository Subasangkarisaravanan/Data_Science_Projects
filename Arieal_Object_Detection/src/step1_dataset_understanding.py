import os
import random
from PIL import Image
import matplotlib.pyplot as plt

# ==============================
# PATH CONFIGURATION
# ==============================

BASE_PATH = r"C:\Users\Siva\PycharmProjects\Aerial_Object\data\classification_dataset"

TRAIN_DIR = os.path.join(BASE_PATH, "train")
VALID_DIR = os.path.join(BASE_PATH, "valid")
TEST_DIR = os.path.join(BASE_PATH, "test")


# ==============================
# FUNCTION 1: Print Folder Structure
# ==============================

def print_folder_structure():
    print("\n===== DATASET FOLDER STRUCTURE =====\n")

    for split in ["train", "valid", "test"]:
        split_path = os.path.join(BASE_PATH, split)
        print(f"{split.upper()} SET:")

        for class_name in os.listdir(split_path):
            class_path = os.path.join(split_path, class_name)
            if os.path.isdir(class_path):
                count = len(os.listdir(class_path))
                print(f"  - {class_name}: {count} images")

        print()

    print("=====================================\n")


# ==============================
# FUNCTION 2: Check Class Imbalance
# ==============================

def check_class_imbalance():
    print("===== CLASS IMBALANCE CHECK (TRAIN SET) =====\n")

    train_counts = {}
    total = 0

    for class_name in os.listdir(TRAIN_DIR):
        class_path = os.path.join(TRAIN_DIR, class_name)
        count = len(os.listdir(class_path))
        train_counts[class_name] = count
        total += count

    for cls, count in train_counts.items():
        percentage = (count / total) * 100
        print(f"{cls}: {count} images ({percentage:.2f}%)")

    print("\nTotal Training Images:", total)
    print("=============================================\n")


# ==============================
# FUNCTION 3: Check Image Dimensions
# ==============================

def check_image_dimensions():
    print("===== SAMPLE IMAGE DIMENSIONS =====\n")

    for class_name in os.listdir(TRAIN_DIR):
        class_path = os.path.join(TRAIN_DIR, class_name)
        sample_image = random.choice(os.listdir(class_path))
        img_path = os.path.join(class_path, sample_image)

        img = Image.open(img_path)
        print(f"{class_name} sample image size: {img.size} (Width x Height)")

    print("=====================================\n")


# ==============================
# FUNCTION 4: Visualize Sample Images
# ==============================

def visualize_samples(samples_per_class=3):
    print("Displaying sample images...\n")

    classes = os.listdir(TRAIN_DIR)
    plt.figure(figsize=(10, 6))
    plot_index = 1

    for class_name in classes:
        class_path = os.path.join(TRAIN_DIR, class_name)
        images = os.listdir(class_path)

        sample_images = random.sample(images, samples_per_class)

        for img_name in sample_images:
            img_path = os.path.join(class_path, img_name)
            img = Image.open(img_path)

            plt.subplot(len(classes), samples_per_class, plot_index)
            plt.imshow(img)
            plt.title(class_name)
            plt.axis("off")

            plot_index += 1

    plt.tight_layout()
    plt.show()


# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    print_folder_structure()
    check_class_imbalance()
    check_image_dimensions()
    visualize_samples()