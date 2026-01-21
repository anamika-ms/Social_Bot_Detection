from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
model = joblib.load("xgboost_bot_model_temporal.pkl")


# Request schema

class BotInput(BaseModel):
    followers_count: int
    following_count: int
    statuses_count: int
    verified: int
    account_age_days: int

# Root endpoint (test)
@app.get("/")
def root():
    return {"message": "Social Bot Detection API is running"}

# Prediction endpoint
@app.post("/predict")
def predict_bot(data: BotInput):

    follow_ratio = data.followers_count / (data.following_count + 1)
    tweets_per_day = data.statuses_count / max(data.account_age_days, 1)
    following_growth_rate = data.following_count / max(data.account_age_days, 1)

    features = [[
        data.followers_count,
        data.following_count,
        data.statuses_count,
        data.verified,
        follow_ratio,
        data.account_age_days,
        tweets_per_day,
        following_growth_rate
    ]]

    prob = model.predict_proba(features)[0][1]
    label = "Bot" if prob >= 0.5 else "Human"

    return {
        "prediction": label,
        "bot_probability": round(float(prob), 3)
    }
