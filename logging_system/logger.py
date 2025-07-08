import os
from datetime import datetime
import cv2
from database.db import insert_visitor, log_event_db

def log_event(face_id, image, event_type):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%H-%M-%S')
    folder = f"logs/{event_type}s/{date}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{face_id}_{timestamp}.jpg"
    path = os.path.join(folder, filename)
    cv2.imwrite(path, image)

    # Log to DB
    insert_visitor(face_id)
    log_event_db(face_id, event_type, path)

    # Also log to events.log
    with open("logging_system/events.log", "a") as log_file:
        log_file.write(f"{now}: {event_type.upper()} - {face_id}\n")
