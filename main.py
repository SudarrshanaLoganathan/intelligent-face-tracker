import os
import cv2
import json
import time
from datetime import datetime
from face_detection.yolo_detector import FaceDetector
from face_recognition.insight_embedder import FaceEmbedder
from logging_system.logger import log_event
from database.db import setup_db
from utils.helpers import cosine_similarity

# Step 1: Initialize
face_db = {}  # face_id: embedding
face_timers = {}  # face_id: last_seen_time
active_faces = set()  # currently tracked faces
unique_id = 1
setup_db()

# Step 2: Load Config
with open('config.json') as f:
    config = json.load(f)

cap = cv2.VideoCapture(config['video_path'])
face_detector = FaceDetector()
face_embedder = FaceEmbedder()
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_faces = set()

    # Step 3: Skip Frames for Performance
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
                if cosine_similarity(embedding, emb) > config['min_cosine_similarity']:
                    matched_id = fid
                    break

            if matched_id is None:
                matched_id = f"face_{unique_id:03}"
                face_db[matched_id] = embedding
                unique_id += 1
                log_event(matched_id, crop, 'entry')

            current_faces.add(matched_id)
            face_timers[matched_id] = time.time()

    # Step 4: Detect Exits
    now = time.time()
    for fid in list(active_faces):
        if fid not in current_faces and now - face_timers.get(fid, now) > 2:
            active_faces.remove(fid)
            log_event(fid, frame, 'exit')

    active_faces.update(current_faces)
    frame_count += 1

    # Step 5: Show Frame (Optional Resize for Small Screens)
    resized_frame = cv2.resize(frame, (720, 480))
    cv2.imshow("Face Tracker", resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()