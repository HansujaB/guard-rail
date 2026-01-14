# import sys
# import numpy as np

# # CRITICAL: Import and register VibrationFeatureExtractor in __main__ namespace
# # This fixes pickle loading issue where class was saved from __main__
# from vibration_features import VibrationFeatureExtractor
# sys.modules['__main__'].VibrationFeatureExtractor = VibrationFeatureExtractor

# # ────────────────────────────────────────────────────────────────
# # CRITICAL FIX FOR YOLO LOADING ERROR
# # Must be BEFORE importing YOLO / torch.load
# # ────────────────────────────────────────────────────────────────
# import torch

# # Import the actual class first, then add it to safe globals
# from ultralytics.nn.tasks import DetectionModel
# torch.serialization.add_safe_globals([DetectionModel])

# from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# import tensorflow as tf
# from tensorflow import keras
# import librosa
# import soundfile as sf
# import io
# import joblib
# from ultralytics import YOLO
# from typing import Optional
# import uvicorn
# import h5py

# app = FastAPI(
#     title="Railway Track Intrusion Detection API",
#     description="Fuses vibration, acoustic, sequence, human detection → computes intent score & alert",
#     version="1.0.0"
# )

# # ========================
# # Model Architecture Definitions (Match training notebooks)
# # ========================
# def build_acoustic_model():
#     """Rebuild acoustic CNN architecture - matches voice-model notebook"""
#     model = keras.Sequential([
#         keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 128, 1)),
#         keras.layers.MaxPooling2D((2, 2)),
#         keras.layers.Conv2D(64, (3, 3), activation='relu'),
#         keras.layers.MaxPooling2D((2, 2)),
#         keras.layers.Conv2D(128, (3, 3), activation='relu'),
#         keras.layers.MaxPooling2D((2, 2)),
#         keras.layers.Flatten(),
#         keras.layers.Dense(128, activation='relu'),
#         keras.layers.Dropout(0.5),
#         keras.layers.Dense(1, activation='sigmoid')
#     ])
#     return model

# def build_lstm_model():
#     """Rebuild LSTM sequence predictor - matches lstm-seq-final notebook"""
#     model = keras.Sequential([
#         keras.layers.LSTM(128, return_sequences=True, input_shape=(60, 1)),
#         keras.layers.Dropout(0.2),
#         keras.layers.LSTM(64),
#         keras.layers.Dropout(0.2),
#         keras.layers.Dense(1)
#     ])
#     return model

# # ========================
# # Load All Models
# # ========================
# print("Loading models...")

# try:
#     # 1. Vibration: Random Forest + Scaler + Feature Extractor
#     rf_model = joblib.load("./models/railway_anomaly_detector.pkl")
#     vib_scaler = joblib.load("./models/scaler.pkl")
#     feature_extractor = joblib.load("./models/feature_extractor.pkl")
#     print("✓ Loaded vibration models")

#     # 2. Acoustic: CNN - Rebuild architecture and load weights
#     try:
#         acoustic_model = build_acoustic_model()
#         acoustic_model.load_weights("./models/acoustic_tool_detector.h5")
#         acoustic_model.compile(optimizer='adam', loss='binary_crossentropy')
#         print("✓ Loaded acoustic model (rebuilt + weights)")
#     except Exception as e:
#         print(f"Acoustic model loading failed: {e}")
#         raise

#     # 3. Sequence: LSTM - Rebuild architecture and load weights
#     try:
#         lstm_model = build_lstm_model()
#         lstm_model.load_weights("./models/lstm_sequence_predictor.h5")
#         lstm_model.compile(optimizer='adam', loss='mse')
#         print("✓ Loaded LSTM model (rebuilt + weights)")
#     except Exception as e:
#         print(f"LSTM model loading failed: {e}")
#         raise

#     # 4. Human: YOLOv11 Nano
#     yolo = YOLO("./models/yolo11n.pt")
#     print("✓ Loaded YOLO model")

#     print("\n✅ All models loaded successfully!")
    
# except Exception as e:
#     print(f"\n❌ Model loading failed: {str(e)}")
#     import traceback
#     traceback.print_exc()
#     raise

# # ========================
# # Constants
# # ========================
# TARGET_SR = 16000
# MEL_SHAPE = (64, 128)
# LSTM_WINDOW = 60
# VIB_FEATURE_COUNT = 20
# INTENT_THRESHOLD = 0.55

# # ========================
# # Helper Functions
# # ========================

# def extract_mel(audio_bytes: bytes) -> np.ndarray:
#     try:
#         with io.BytesIO(audio_bytes) as f:
#             audio, sr = sf.read(f)
#         if audio.ndim > 1:
#             audio = np.mean(audio, axis=1)
#         if sr != TARGET_SR:
#             audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)
#         mel = librosa.feature.melspectrogram(
#             y=audio, sr=TARGET_SR, n_mels=64, n_fft=1024, hop_length=512
#         )
#         mel_db = librosa.power_to_db(mel, ref=np.max)
#         if mel_db.shape[1] < MEL_SHAPE[1]:
#             mel_db = np.pad(mel_db, ((0, 0), (0, MEL_SHAPE[1] - mel_db.shape[1])))
#         else:
#             mel_db = mel_db[:, :MEL_SHAPE[1]]
#         return mel_db
#     except Exception as e:
#         raise ValueError(f"Audio processing failed: {str(e)}")

# def get_vibration_score(vibration_str: str) -> float:
#     try:
#         vib_array = np.array([float(x) for x in vibration_str.split(',')])
#         if len(vib_array) < 100:
#             raise ValueError("Vibration data too short")

#         features = feature_extractor.extract(vib_array)
#         if len(features) != VIB_FEATURE_COUNT:
#             raise ValueError(f"Expected {VIB_FEATURE_COUNT} features, got {len(features)}")

#         features_scaled = vib_scaler.transform([features])
#         prob = rf_model.predict_proba(features_scaled)[0][1]
#         return float(prob)
#     except Exception as e:
#         raise ValueError(f"Vibration processing failed: {str(e)}")

# def get_acoustic_score(audio_bytes: bytes) -> float:
#     mel = extract_mel(audio_bytes)
#     input_data = mel[np.newaxis, ..., np.newaxis]
#     prob = acoustic_model.predict(input_data, verbose=0)[0][0]
#     return float(prob)

# def get_temporal_score(sequence_str: str) -> float:
#     try:
#         seq = np.array([float(x) for x in sequence_str.split(',')])
#         if len(seq) != LSTM_WINDOW:
#             raise ValueError(f"Sequence must have {LSTM_WINDOW} values")

#         input_seq = seq.reshape(1, LSTM_WINDOW, 1)
#         pred = lstm_model.predict(input_seq, verbose=0).flatten()[0]
#         actual = seq[-1]
#         error = abs(pred - actual)
#         prob = 1 / (1 + np.exp(-(error - 0.05) / 0.02))
#         return float(prob)
#     except Exception as e:
#         raise ValueError(f"Sequence processing failed: {str(e)}")

# def get_human_score(pir: int, image_bytes: Optional[bytes] = None) -> float:
#     human_prob = float(pir)

#     if image_bytes:
#         try:
#             with io.BytesIO(image_bytes) as f_img:
#                 results = yolo(f_img, verbose=False)
#                 for r in results:
#                     for box in r.boxes:
#                         if int(box.cls) == 0:
#                             conf = float(box.conf)
#                             human_prob = max(human_prob, conf)
#         except:
#             pass

#     return human_prob

# def get_context_score(weather_ignore: bool) -> float:
#     return 0.0 if weather_ignore else 1.0

# # ========================
# # Main Endpoint
# # ========================
# @app.post("/predict/intent")
# async def predict_intent(
#     vibration: str = Form(..., description="Comma separated vibration values"),
#     acoustic_file: UploadFile = File(..., description="Audio chunk .wav (5-10s)"),
#     sequence: str = Form(..., description="Comma separated sequence values for LSTM (60 values)"),
#     pir: int = Form(..., ge=0, le=1, description="PIR state: 0 or 1"),
#     image_file: Optional[UploadFile] = File(None, description="Optional CCTV/drone image .jpg"),
#     weather_ignore: bool = Form(False, description="Weather/context filter: true=ignore event")
# ):
#     try:
#         audio_bytes = await acoustic_file.read()
#         image_bytes = await image_file.read() if image_file else None

#         vib_score = get_vibration_score(vibration)
#         acous_score = get_acoustic_score(audio_bytes)
#         temp_score = get_temporal_score(sequence)
#         human_score = get_human_score(pir, image_bytes)
#         context_score = get_context_score(weather_ignore)

#         intent = (
#             0.35 * vib_score +
#             0.30 * acous_score +
#             0.20 * human_score +
#             0.10 * temp_score +
#             0.05 * context_score
#         )

#         reasons = []
#         if vib_score > 0.5: reasons.append(f"Abnormal vibration (score: {vib_score:.2f})")
#         if acous_score > 0.5: reasons.append(f"Tool-like acoustic pattern (score: {acous_score:.2f})")
#         if human_score > 0.5: reasons.append(f"Human presence detected (score: {human_score:.2f})")
#         if temp_score > 0.5: reasons.append(f"Unplanned sequence detected (score: {temp_score:.2f})")
#         if context_score < 0.5: reasons.append("Event ignored due to weather/context")

#         alert = None
#         if intent > 0.5:
#             alert = {
#                 "alert_id": "ALT-221",
#                 "risk": "high" if intent > 0.75 else "medium",
#                 "intent_score": round(intent, 3),
#                 "reason": reasons
#             }

#         return {
#             "intent_score": round(intent, 3),
#             "individual_scores": {
#                 "vibration_anomaly": round(vib_score, 3),
#                 "acoustic_tool": round(acous_score, 3),
#                 "human_presence": round(human_score, 3),
#                 "temporal_unplanned": round(temp_score, 3),
#                 "context": round(context_score, 3)
#             },
#             "reasons": reasons,
#             "alert_triggered": alert is not None,
#             "alert": alert
#         }

#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))

# @app.get("/health")
# async def health():
#     return {"status": "healthy", "models": "all loaded"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

import sys
import numpy as np

# CRITICAL: Import and register VibrationFeatureExtractor in __main__ namespace
# This fixes pickle loading issue where class was saved from __main__
from vibration_features import VibrationFeatureExtractor
sys.modules['__main__'].VibrationFeatureExtractor = VibrationFeatureExtractor

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import tensorflow as tf
from tensorflow import keras
import librosa
import soundfile as sf
import io
import joblib
from typing import Optional
import uvicorn
import h5py

app = FastAPI(
    title="Railway Track Intrusion Detection API",
    description="Fuses vibration, acoustic, sequence, human detection → computes intent score & alert",
    version="1.0.0"
)

# ========================
# Model Architecture Definitions (Match training notebooks)
# ========================
def build_acoustic_model():
    """Rebuild acoustic CNN architecture - matches voice-model notebook"""
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 128, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(128, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    return model

def build_lstm_model():
    """Rebuild LSTM sequence predictor - matches lstm-seq-final notebook"""
    model = keras.Sequential([
        keras.layers.LSTM(128, return_sequences=True, input_shape=(60, 1)),
        keras.layers.Dropout(0.2),
        keras.layers.LSTM(64),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1)
    ])
    return model

# ========================
# Load All Models
# ========================
print("Loading models...")

try:
    # 1. Vibration: Random Forest + Scaler + Feature Extractor
    rf_model = joblib.load("./models/railway_anomaly_detector.pkl")
    vib_scaler = joblib.load("./models/scaler.pkl")
    feature_extractor = joblib.load("./models/feature_extractor.pkl")
    print("✓ Loaded vibration models")

    # 2. Acoustic: CNN - Rebuild architecture and load weights
    try:
        acoustic_model = build_acoustic_model()
        acoustic_model.load_weights("./models/acoustic_tool_detector.h5")
        acoustic_model.compile(optimizer='adam', loss='binary_crossentropy')
        print("✓ Loaded acoustic model (rebuilt + weights)")
    except Exception as e:
        print(f"Acoustic model loading failed: {e}")
        raise

    # 3. Sequence: LSTM - Rebuild architecture and load weights
    try:
        lstm_model = build_lstm_model()
        lstm_model.load_weights("./models/lstm_sequence_predictor.h5")
        lstm_model.compile(optimizer='adam', loss='mse')
        print("✓ Loaded LSTM model (rebuilt + weights)")
    except Exception as e:
        print(f"LSTM model loading failed: {e}")
        raise

    print("\n✅ All models loaded successfully!")
    print("📌 Note: YOLO disabled - using PIR-only for human detection")
    
except Exception as e:
    print(f"\n❌ Model loading failed: {str(e)}")
    import traceback
    traceback.print_exc()
    raise

# ========================
# Constants
# ========================
TARGET_SR = 16000
MEL_SHAPE = (64, 128)
LSTM_WINDOW = 60
VIB_FEATURE_COUNT = 20
INTENT_THRESHOLD = 0.55

# ========================
# Helper Functions
# ========================

def extract_mel(audio_bytes: bytes) -> np.ndarray:
    try:
        with io.BytesIO(audio_bytes) as f:
            audio, sr = sf.read(f)
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)
        if sr != TARGET_SR:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)
        mel = librosa.feature.melspectrogram(
            y=audio, sr=TARGET_SR, n_mels=64, n_fft=1024, hop_length=512
        )
        mel_db = librosa.power_to_db(mel, ref=np.max)
        if mel_db.shape[1] < MEL_SHAPE[1]:
            mel_db = np.pad(mel_db, ((0, 0), (0, MEL_SHAPE[1] - mel_db.shape[1])))
        else:
            mel_db = mel_db[:, :MEL_SHAPE[1]]
        return mel_db
    except Exception as e:
        raise ValueError(f"Audio processing failed: {str(e)}")

def get_vibration_score(vibration_str: str) -> float:
    try:
        vib_array = np.array([float(x) for x in vibration_str.split(',')])
        if len(vib_array) < 100:
            raise ValueError("Vibration data too short")

        features = feature_extractor.extract(vib_array)
        if len(features) != VIB_FEATURE_COUNT:
            raise ValueError(f"Expected {VIB_FEATURE_COUNT} features, got {len(features)}")

        features_scaled = vib_scaler.transform([features])
        prob = rf_model.predict_proba(features_scaled)[0][1]
        return float(prob)
    except Exception as e:
        raise ValueError(f"Vibration processing failed: {str(e)}")

def get_acoustic_score(audio_bytes: bytes) -> float:
    mel = extract_mel(audio_bytes)
    input_data = mel[np.newaxis, ..., np.newaxis]
    prob = acoustic_model.predict(input_data, verbose=0)[0][0]
    return float(prob)

def get_temporal_score(sequence_str: str) -> float:
    try:
        seq = np.array([float(x) for x in sequence_str.split(',')])
        if len(seq) != LSTM_WINDOW:
            raise ValueError(f"Sequence must have {LSTM_WINDOW} values")

        input_seq = seq.reshape(1, LSTM_WINDOW, 1)
        pred = lstm_model.predict(input_seq, verbose=0).flatten()[0]
        actual = seq[-1]
        error = abs(pred - actual)
        prob = 1 / (1 + np.exp(-(error - 0.05) / 0.02))
        return float(prob)
    except Exception as e:
        raise ValueError(f"Sequence processing failed: {str(e)}")

def get_human_score(pir: int, image_bytes: Optional[bytes] = None) -> float:
    """
    Human detection using PIR sensor only.
    YOLO image detection disabled - returns PIR value directly.
    """
    return float(pir)

def get_context_score(weather_ignore: bool) -> float:
    return 0.0 if weather_ignore else 1.0

# ========================
# Main Endpoint
# ========================
@app.post("/predict/intent")
async def predict_intent(
    vibration: str = Form(..., description="Comma separated vibration values"),
    acoustic_file: UploadFile = File(..., description="Audio chunk .wav (5-10s)"),
    sequence: str = Form(..., description="Comma separated sequence values for LSTM (60 values)"),
    pir: int = Form(..., ge=0, le=1, description="PIR state: 0 or 1"),
    image_file: Optional[UploadFile] = File(None, description="Optional CCTV/drone image .jpg"),
    weather_ignore: bool = Form(False, description="Weather/context filter: true=ignore event")
):
    try:
        audio_bytes = await acoustic_file.read()
        image_bytes = await image_file.read() if image_file else None

        vib_score = get_vibration_score(vibration)
        acous_score = get_acoustic_score(audio_bytes)
        temp_score = get_temporal_score(sequence)
        human_score = get_human_score(pir, image_bytes)
        context_score = get_context_score(weather_ignore)

        intent = (
            0.35 * vib_score +
            0.30 * acous_score +
            0.20 * human_score +
            0.10 * temp_score +
            0.05 * context_score
        )

        reasons = []
        if vib_score > 0.5: reasons.append(f"Abnormal vibration (score: {vib_score:.2f})")
        if acous_score > 0.5: reasons.append(f"Tool-like acoustic pattern (score: {acous_score:.2f})")
        if human_score > 0.5: reasons.append(f"Human presence detected (score: {human_score:.2f})")
        if temp_score > 0.5: reasons.append(f"Unplanned sequence detected (score: {temp_score:.2f})")
        if context_score < 0.5: reasons.append("Event ignored due to weather/context")

        alert = None
        if intent > 0.5:
            alert = {
                "alert_id": "ALT-221",
                "risk": "high" if intent > 0.75 else "medium",
                "intent_score": round(intent, 3),
                "reason": reasons
            }

        return {
            "intent_score": round(intent, 3),
            "individual_scores": {
                "vibration_anomaly": round(vib_score, 3),
                "acoustic_tool": round(acous_score, 3),
                "human_presence": round(human_score, 3),
                "temporal_unplanned": round(temp_score, 3),
                "context": round(context_score, 3)
            },
            "reasons": reasons,
            "alert_triggered": alert is not None,
            "alert": alert
        }

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "models": "all loaded"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)