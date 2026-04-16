import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active! Use /weather/{city} to get data."}

@app.get("/weather/{city}")
def get_weather(city: str):
    return {
        "city": city, 
        "temp": "28°C", 
        "condition": "Partly Cloudy",
        "location": f"{city.capitalize()}, Nigeria"
    }

@app.get("/forecast")
def get_forecast(city: str = "Lagos"):
    return {"city": city, "forecast": "Sunny intervals expected."}

@app.get("/news")
def get_news():
    return {"articles": [{"title": "Lagos Weather Update", "content": "Clear skies over UNILAG today."}]}

@app.get("/exchange-rate")
def get_exchange_rate(base: str = "NGN"):
    return {"base": base, "rates": {"USD": 0.00065}}
@app.get("/forecast")
def get_forecast(city: str):
    return {"detail": "Forecast data coming soon for " + city}

@app.get("/news")
def get_news():
    return {"articles": []}

@app.get("/exchange-rate")
def get_exchange_rate(base: str = "NGN"):
    return {"rates": {"USD": 0.00065}, "base": base}
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active! Use /weather/{city} to get data."}

@app.get("/weather/{city}")
def get_weather(city: str):
    # This is a placeholder to ensure the API starts successfully
    return {
        "city": city, 
        "temp": "28°C", 
        "condition": "Partly Cloudy",
        "location": "Lagos, Nigeria"
    }
