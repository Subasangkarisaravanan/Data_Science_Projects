from ultralytics import YOLO

print("\n========== STEP 8B: YOLOv8 INFERENCE ==========\n")

model = YOLO("C:/Users/Siva/PycharmProjects/Aerial_Object/src/runs/detect/yolov8_bird_drone2/weights/best.pt")

# Run inference on test images
results = model.predict(
    source="C:/Users/Siva/PycharmProjects/Aerial_Object/data/object_detection_dataset/test/images",
    imgsz=640,
    conf=0.25,
    save=True
)

print("\nInference Complete. Check 'runs/detect/predict' folder for results.\n")