import cv2
import json
import time
from face_detection.yolo_detector import FaceDetector
from face_recognition.insight_embedder import FaceEmbedder
from logging_system.logger import log_event
from database.db import setup_db
from utils.helpers import cosine_similarity

# Initialize database
setup_db()

# Load config
with open('config.json') as f:
    config = json.load(f)

# Decide input source
source = config['video_path'] if not config.get('use_camera', False) else 0
cap = cv2.VideoCapture(source)

# Initialize components
face_detector = FaceDetector()
face_embedder = FaceEmbedder()

face_db = {}          # face_id: embedding
face_timers = {}      # face_id: last seen time
active_faces = set()  # currently visible face_ids
unique_id = 1
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_faces = set()

    if frame_count % config['detection_frame_skip'] == 0:
        boxes = face_detector.detect(frame)
        for box in boxes:
            x1, y1, x2, y2 = box
            crop = frame[y1:y2, x1:x2]
            embedding = face_embedder.get_embedding(crop)

            if embedding is None:
                continue

            matched_id = None
            for fid, emb in face_db.items():
                similarity = cosine_similarity(embedding, emb)
                if similarity > config['min_cosine_similarity']:
                    matched_id = fid
                    break

            if matched_id is None:
                matched_id = f"face_{unique_id:03}"
                face_db[matched_id] = embedding
                unique_id += 1
                log_event(matched_id, crop, 'entry')
                print(f"[INFO] Registered new face: {matched_id}")

            current_faces.add(matched_id)
            face_timers[matched_id] = time.time()

    # Face exit logic
    now = time.time()
    for fid in list(active_faces):
        if fid not in current_faces and now - face_timers.get(fid, now) > 2:
            active_faces.remove(fid)
            log_event(fid, frame, 'exit')

    active_faces.update(current_faces)
    frame_count += 1

    # Overlay live face count
    cv2.putText(frame, f"Unique Faces: {len(face_db)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Resize frame to fit in window
    target_width = 800
    height, width = frame.shape[:2]
    scaling_factor = target_width / float(width)
    resized_frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor)

    cv2.imshow("Live Face Tracker", resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
