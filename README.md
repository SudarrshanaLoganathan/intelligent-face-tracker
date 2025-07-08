# Intelligent Face Tracker with Auto-Registration and Visitor Counting

This project is an AI-driven real-time face tracking and visitor counting system that:
- Detects faces using **YOLOv8**
- Generates embeddings with **InsightFace**
- Tracks users using **DeepSort**
- Automatically registers unique visitors
- Logs entries and exits with timestamps, cropped images, and metadata
- Stores logs in a structured filesystem and **SQLite database**

---

## 🚀 Features

- Real-time face detection, recognition, and tracking  
- Auto-registration of new visitors  
- Entry/Exit detection with timestamped logging  
- Visitor metadata saved to database  
- Cropped face image storage  
- Frame-skipping controlled via `config.json`  

---

## 🏗️ Project Structure

