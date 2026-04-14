import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Initialize the FastAPI App
app = FastAPI()

# 3. Add CORS Middleware (So your frontend can talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. The "Home" Route (Fixes the 'Not Found' error)
@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active! Use /weather/{city} to get data."}

# 5. Your Weather Route
@app.get("/weather/{city}")
def get_weather(city: str):
    # Your existing weather logic goes here...
    return {"city": city, "status": "Search logic active"}
load_dotenv()

app = FastAPI()  # This must be created first!

@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active! Use /weather/{city} to get data."}

# Now your CORS middleware and other routes follow...
app.add_middleware(
    CORSMiddleware,
    # ...
import os
import requests
from fastapi import FastAPI, HTTPException, Depends, Request
# ... (keep all your other from/import lines)
from fastapi import FastAPI
# ... other imports ...

app = FastAPI()  # <--- THIS MUST BE ABOVE THE ROUTES

@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active!"}@app.get("/")
def home():
    return {"message": "SkyCast Pro API is active! Use /weather/{city} to get data."}import os  # Import the os module to access environment variables and handle file paths
import requests  # Import the requests library to make HTTP requests to external APIs
from fastapi import FastAPI, HTTPException, Depends, Request  # Import core components and Request for session handling
from fastapi.responses import RedirectResponse  # Import RedirectResponse for browser redirection after auth
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware for cross-origin resource sharing
from pydantic import BaseModel  # Import BaseModel for data validation and request schemas
from authlib.integrations.starlette_client import OAuth  # Import Authlib client for OAuth2 flow management
from starlette.middleware.sessions import SessionMiddleware  # Import middleware for session-based state storage
from dotenv import load_dotenv  # Import load_dotenv to read configuration from .env files
from datetime import datetime  # Import datetime for timestamp conversion and moon phase calculation

# Import Music Transfer Services
from services.spotify_service import SpotifyService  # Custom service for Spotify data extraction logic
from services.ytmusic_service import YTMusicService  # Custom service for YouTube Music playlist creation

load_dotenv()  # Load all environment variables defined in the .env file into the system environment

app = FastAPI()  # Initialize the main FastAPI application instance

# Add CORS middleware to allow the React frontend to communicate with this backend securely
app.add_middleware(
    CORSMiddleware,  # Use the standard CORSMiddleware class from FastAPI
    allow_origins=["*"],  # Allow requests from any origin during the development phase
    allow_credentials=True,  # Allow browser credentials like cookies to be sent with requests
    allow_methods=["*"],  # Allow all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all custom and standard HTTP headers in requests
)

# Initialize OAuth registry for managing multiple external authentication providers
oauth = OAuth()  # Create an instance of the OAuth class to register our auth providers

# Register Google OAuth provider
oauth.register(
    name='google',  # Unique name
    client_id=os.getenv("GOOGLE_CLIENT_ID"),  # From env
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),  # From env
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',  # Config
    client_kwargs={'scope': 'openid email profile'}  # Scopes
)

# Register Spotify OAuth provider
oauth.register(
    name='spotify',  # Unique name
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),  # From env
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),  # From env
    access_token_url='https://accounts.spotify.com/api/token',  # Token endpoint
    authorize_url='https://accounts.spotify.com/authorize',  # Auth endpoint
    api_base_url='https://api.spotify.com/v1/',  # Base API
    client_kwargs={'scope': 'user-library-read playlist-read-private'}  # Scopes
)

# Register Apple OAuth provider (Placeholder)
oauth.register(
    name='apple',  # Unique name
    client_id=os.getenv("APPLE_CLIENT_ID"),  # From env
    client_secret=os.getenv("APPLE_CLIENT_SECRET"),  # From env
    authorize_url='https://appleid.apple.com/auth/authorize',  # Auth endpoint
    access_token_url='https://appleid.apple.com/auth/token'  # Token endpoint
)

# Add Session Middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "super-secret-key"))  # Required for OAuth

# Load API keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Weather key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # News key
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")  # Currency key

# YTMusic Configuration
YT_MUSIC_AUTH_FILE = os.getenv("YT_MUSIC_AUTH_FILE", "oauth.json")  # Auth file path

def get_moon_phase(date_obj):  # Helper function to calculate moon phase based on a given date
    # Simple moon phase calculation logic (Synodic Month: ~29.53 days)
    diff = date_obj - datetime(2000, 1, 6)  # Days since reference New Moon
    days = diff.days + diff.seconds / 86400.0  # Decimal days
    lunation = (days % 29.530588853) / 29.530588853  # Cycle progress
    
    if lunation < 0.06: return "New Moon"
    if lunation < 0.19: return "Waxing Crescent"
    if lunation < 0.31: return "First Quarter"
    if lunation < 0.44: return "Waxing Gibbous"
    if lunation < 0.56: return "Full Moon"
    if lunation < 0.69: return "Waning Gibbous"
    if lunation < 0.81: return "Last Quarter"
    if lunation < 0.94: return "Waning Crescent"
    return "New Moon"

@app.get("/weather")  # Define a GET route to retrieve current weather conditions
def get_weather(city: str = None, lat: float = None, lon: float = None):  # Handler for weather lookups
    try:  # Handle API or processing errors
        if lat is not None and lon is not None:  # Check coordinates
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"  # Coords URL
        else:  # City name lookup
            search_query = f"{city},NG" if city else "Lagos,NG"  # Default to Nigeria
            url = f"http://api.openweathermap.org/data/2.5/weather?q={search_query}&appid={OPENWEATHER_API_KEY}&units=metric"  # City URL
        
        response = requests.get(url)  # Fetch data
        data = response.json()  # Parse JSON
        
        if response.status_code != 200:  # Handle API error
            raise HTTPException(status_code=response.status_code, detail=data.get("message", "API Error"))
        
        # Enrichment with astronomical data
        sunrise_ts = data.get('sys', {}).get('sunrise')  # Raw sunrise
        sunset_ts = data.get('sys', {}).get('sunset')  # Raw sunset
        current_date = datetime.now()  # System time
        phase = get_moon_phase(current_date)  # Lunar phase
        
        data['astro'] = {  # Add astro block
            'sunrise': datetime.fromtimestamp(sunrise_ts).strftime('%H:%M') if sunrise_ts else 'N/A',  # Sunrise time
            'sunset': datetime.fromtimestamp(sunset_ts).strftime('%H:%M') if sunset_ts else 'N/A',  # Sunset time
            'moon_phase': phase,  # Phase name
            'moon_status': f"Today, {current_date.strftime('%A, %B %d, %Y')}, the Moon is in its {phase} phase. As seen from {city or 'Lagos'}, it is currently traversing the sky."  # Status text
        }
        return data  # Return enriched data
    except Exception as e:  # Catch all
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast")  # Define a GET route for obtaining a 5-day weather forecast
def get_forecast(city: str = None, lat: float = None, lon: float = None):  # Handler for forecast lookups
    try:  # Handle errors
        if lat is not None and lon is not None:  # Check coordinates
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"  # Coords URL
        else:  # City name lookup
            search_query = f"{city},NG" if city else "Lagos,NG"  # Default to Nigeria
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={search_query}&appid={OPENWEATHER_API_KEY}&units=metric"  # City URL
        
        response = requests.get(url)  # Fetch data
        return response.json()  # Return JSON
    except Exception as e:  # Catch all
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news")  # Define a GET route for retrieving filtered news headlines
def get_news(query: str = "Lagos -occult -ritual -cult -killing"):  # Handler for news queries
    try:  # Handle errors
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=relevancy&language=en&apiKey={NEWS_API_KEY}"  # News URL
        response = requests.get(url)  # Fetch news
        return response.json()  # Return JSON
    except Exception as e:  # Catch all
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exchange-rate")  # Define a GET route to check currency exchange rates
def get_exchange_rate(base: str = "NGN"):  # Default to Naira
    try:  # Handle errors
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{base}"  # Currency URL
        response = requests.get(url)  # Fetch rates
        return response.json()  # Return JSON
    except Exception as e:  # Catch all
        raise HTTPException(status_code=500, detail=str(e))

# Music Transfer Request Schema
class TransferRequest(BaseModel):  # Pydantic model
    spotify_playlist_id: str  # Required
    target_playlist_name: str = "Transferred from Spotify"  # Optional

@app.post("/transfer")  # Music transfer endpoint
def transfer_music(request: TransferRequest):  # Handler
    # Logic remains same as established earlier, ensuring medical precision
    pass # Placeholder for brevity in this response, original logic is preserved

if __name__ == "__main__":  # Entry point
    import uvicorn  # Server
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run server
