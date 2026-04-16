from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# STEP 1: Create the app FIRST
app = FastAPI()

# STEP 2: Configure security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STEP 3: Define routes ONLY after app exists
@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active!"}

@app.get("/weather/{city}")
def get_weather(city: str):
    return {"city": city, "temp": "28°C", "condition": "Partly Cloudy"}

@app.get("/forecast")
def get_forecast(city: str = "Lagos"):
    return {"city": city, "forecast": "Sunny intervals"}

@app.get("/news")
def get_news():
    return {"articles": []}

@app.get("/exchange-rate")
def get_exchange_rate():
    return {"base": "NGN", "rates": {"USD": 0.00065}}
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Load configuration
load_dotenv()

# 2. Initialize the app (This MUST stay here at the top)
app = FastAPI()

# 3. Security settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Your Routes
@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active!"}

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
    return {"city": city, "forecast": "Sunny intervals expected over the next 24 hours."}

@app.get("/news")
def get_news():
    return {"articles": [{"title": "Meteorology Update", "content": "Analyzing local humidity patterns in Lagos."}]}

@app.get("/exchange-rate")
def get_exchange_rate(base: str = "NGN"):
    return {"base": base, "rates": {"USD": 0.00065}}
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
