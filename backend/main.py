from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
import librosa
import soundfile as sf
import io
import joblib
from ultralytics import YOLO
from typing import Optional
import uvicorn

app = FastAPI(
    title="Railway Track Intrusion Detection API",
    description="Fuses vibration, acoustic, sequence, human detection → computes intent score & alert",
    version="1.0.0"
)

# ========================
# Load All Models
# ========================
print("Loading models...")

# 1. Vibration: Random Forest + Scaler + Feature Extractor
rf_model = joblib.load("./models/railway_anomaly_detector.pkl")
vib_scaler = joblib.load("./models/scaler.pkl")
feature_extractor = joblib.load("./models/feature_extractor.pkl")  # your custom class/function

# 2. Acoustic: CNN
acoustic_model = tf.keras.models.load_model("./models/acoustic_tool_detector.h5")

# 3. Sequence: LSTM
lstm_model = tf.keras.models.load_model("./models/lstm_sequence_predictor.h5")

# 4. Human: YOLOv11 Nano (pre-trained) + PIR fallback
yolo = YOLO("yolov11n.pt")  # auto-downloads

print("All models loaded successfully!")

# ========================
# Constants (match your training)
# ========================
TARGET_SR = 16000
MEL_SHAPE = (64, 128)
LSTM_WINDOW = 60       # from your LSTM training
VIB_FEATURE_COUNT = 20 # adjust to match your feature extractor output size
INTENT_THRESHOLD = 0.55  # tune based on testing

# ========================
# Helper Functions
# ========================

def extract_mel(audio_bytes: bytes) -> np.ndarray:
    """Audio → Mel spectrogram (same as training)"""
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
    """Vibration array → features → RF prob of anomaly"""
    try:
        vib_array = np.array([float(x) for x in vibration_str.split(',')])
        if len(vib_array) < 100:  # minimal length check
            raise ValueError("Vibration data too short")

        # Extract features (your custom logic)
        features = feature_extractor.extract(vib_array)  # adjust method name if different
        if len(features) != VIB_FEATURE_COUNT:
            raise ValueError(f"Expected {VIB_FEATURE_COUNT} features, got {len(features)}")

        features_scaled = vib_scaler.transform([features])
        prob = rf_model.predict_proba(features_scaled)[0][1]  # prob of anomaly class
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
        # Sigmoid soft score (tune center/scale)
        prob = 1 / (1 + np.exp(-(error - 0.05) / 0.02))
        return float(prob)
    except Exception as e:
        raise ValueError(f"Sequence processing failed: {str(e)}")

def get_human_score(pir: int, image_bytes: Optional[bytes] = None) -> float:
    human_prob = float(pir)  # PIR base (0 or 1)

    if image_bytes:
        try:
            with io.BytesIO(image_bytes) as f_img:
                results = yolo(f_img, verbose=False)
                for r in results:
                    for box in r.boxes:
                        if int(box.cls) == 0:  # person class
                            conf = float(box.conf)
                            human_prob = max(human_prob, conf)
        except:
            pass  # fallback to PIR if image fails

    return human_prob

def get_context_score(weather_ignore: bool) -> float:
    return 0.0 if weather_ignore else 1.0

# ========================
# Main Endpoint
# ========================
@app.post("/predict/intent")
async def predict_intent(
    vibration: str = Form(..., description="Comma separated vibration values (e.g. 0.1,0.2,...)"),
    acoustic_file: UploadFile = File(..., description="Audio chunk .wav (5-10s)"),
    sequence: str = Form(..., description="Comma separated sequence values for LSTM (60 values)"),
    pir: int = Form(..., ge=0, le=1, description="PIR state: 0 or 1"),
    image_file: Optional[UploadFile] = File(None, description="Optional CCTV/drone image .jpg"),
    weather_ignore: bool = Form(False, description="Weather/context filter: true=ignore event")
):
    try:
        # Read files
        audio_bytes = await acoustic_file.read()
        image_bytes = await image_file.read() if image_file else None

        # Get scores (0-1)
        vib_score = get_vibration_score(vibration)
        acous_score = get_acoustic_score(audio_bytes)
        temp_score = get_temporal_score(sequence)
        human_score = get_human_score(pir, image_bytes)
        context_score = get_context_score(weather_ignore)

        # Intent Fusion
        intent = (
            0.35 * vib_score +
            0.30 * acous_score +
            0.20 * human_score +
            0.10 * temp_score +
            0.05 * context_score
        )

        # XAI Reasons
        reasons = []
        if vib_score > 0.5:   reasons.append(f"Abnormal vibration (score: {vib_score:.2f})")
        if acous_score > 0.5: reasons.append(f"Tool-like acoustic pattern (score: {acous_score:.2f})")
        if human_score > 0.5: reasons.append(f"Human presence detected (score: {human_score:.2f})")
        if temp_score > 0.5:  reasons.append(f"Unplanned sequence detected (score: {temp_score:.2f})")
        if context_score < 0.5: reasons.append("Event ignored due to weather/context")

        # Alert
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