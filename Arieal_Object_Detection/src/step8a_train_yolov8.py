from ultralytics import YOLO

print("\n========== STEP 8A: TRAIN YOLOv8 ==========\n")

model = YOLO("yolov8n.pt")  # Nano model (best for CPU)

model.train(
    data="C:/Users/Siva/PycharmProjects/Aerial_Object/data/object_detection_dataset/data.yaml",
    epochs=15,
    imgsz=640,
    batch=8,
    device="cpu",
    name="yolov8_bird_drone"
)

print("\nYOLOv8 Training Completed Successfully.\n")