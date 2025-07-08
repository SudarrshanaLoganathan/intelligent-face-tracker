from ultralytics import YOLO

class FaceDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)[0]
        return [list(map(int, box.xyxy[0])) for box in results.boxes]
