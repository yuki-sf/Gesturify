import sys
import os
import base64
import string
import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import keras
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

app = FastAPI()

app.mount("/dataset", StaticFiles(directory="dataset"), name="dataset")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
model = None
for model_name in ["model.keras", "model.h5"]:
    if os.path.exists(model_name):
        try:
            model = keras.models.load_model(model_name)
            print(f"Successfully loaded: {model_name}")
            break
        except Exception as e:
            print(f"Could not load {model_name}: {e}")

if model is None:
    print("CRITICAL ERROR: No model file (.h5 or .keras) found in folder!")
    sys.exit(1)

# Mediapipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Label Map
alphabet = ['1','2','3','4','5','6','7','8','9'] + list(string.ascii_uppercase)

def process_frame(base64_string):
    try:
        # Strip metadata header
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        
        # Decode Image
        img_data = base64.b64decode(base64_string)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None: return "Frame Error"

        # MediaPipe Logic
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get 21 Landmarks
                landmark_list = [[lm.x, lm.y] for lm in hand_landmarks.landmark]
                
                # Pre-processing (Relative to Wrist)
                base_x, base_y = landmark_list[0][0], landmark_list[0][1]
                temp_list = []
                for x, y in landmark_list:
                    temp_list.extend([x - base_x, y - base_y])
                
                # Normalization
                max_val = max(map(abs, temp_list))
                if max_val != 0:
                    temp_list = [n / max_val for n in temp_list]
                
                # Model Prediction
                prediction = model.predict(np.array([temp_list]), verbose=0)
                return alphabet[np.argmax(prediction)]
        
        return "No Hand"
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/")
async def get():
    return FileResponse("gesturify.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            result = process_frame(data)
            await websocket.send_text(result)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket Error: {e}")