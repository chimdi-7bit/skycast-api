# Plan: Personal Dashboard and Weather App Implementation

## Objective
Implement two web applications: a **Personal Dashboard** and a **Weather App**, using a React (TypeScript) frontend and a Python (FastAPI) backend. This allows for a modern, responsive UI while leveraging Python for data processing and API integration, which the user is currently learning.

## Background & Motivation
The user previously started these projects on their "gemini cli account" but they are missing from the current local system. The dashboard should display the current date, local weather, local news, and the local dollar exchange rate. The weather app will be a standalone, more detailed version of the weather component.

## Proposed Solution
- **Backend:** A unified FastAPI (Python) backend to handle API requests for weather, news, and exchange rates.
- **Frontend 1 (Dashboard):** A React (TypeScript) application displaying key information at a glance.
- **Frontend 2 (Weather App):** A standalone React (TypeScript) application focusing on detailed weather information.
- **Comments:** EVERY single line of code will include a descriptive comment as per the user's global preference.

## Implementation Plan

### Phase 1: Shared Python Backend (API)
1.  **Project Initialization:**
    - Create an `api/` directory.
    - Set up a Python virtual environment.
    - Install dependencies: `fastapi`, `uvicorn`, `requests`, `python-dotenv`.
2.  **API Integration:**
    - Create a `.env` file to store API keys for OpenWeatherMap, NewsAPI, and ExchangeRate-API.
    - Implement a `main.py` with endpoints for `/weather`, `/news`, and `/exchange-rate`.
3.  **Code Structure:**
    - Each line of the FastAPI implementation will have a comment explaining its purpose.

### Phase 2: Personal Dashboard (React/TS)
1.  **Project Initialization:**
    - Create a `dashboard/` directory.
    - Initialize a React project using Vite with the TypeScript template.
2.  **Component Development:**
    - `DateTimeWidget.tsx`: Displays the current date and time.
    - `WeatherWidget.tsx`: Fetches and displays weather from the FastAPI backend.
    - `NewsWidget.tsx`: Fetches and displays local news.
    - `ExchangeRateWidget.tsx`: Fetches and displays the dollar exchange rate.
3.  **Styling:**
    - Use Vanilla CSS for a modern, dashboard-like layout (cards, grid system).
4.  **Code Structure:**
    - Every line of the React/TypeScript code will have a comment.

### Phase 3: Weather Site/App (React/TS)
1.  **Project Initialization:**
    - Create a `weather-site/` directory.
    - Initialize a React project using Vite with the TypeScript template.
2.  **Detailed Interface:**
    - Build a multi-day forecast view.
    - Add detailed metrics like humidity, wind speed, and UV index.
    - Implement a location search feature.
3.  **Code Structure:**
    - Every line of the code will have a comment.

## Verification & Testing
1.  **Backend Verification:** Test the `/weather`, `/news`, and `/exchange-rate` endpoints using `curl` or FastAPI's auto-generated docs (`/docs`).
2.  **Frontend Integration:** Ensure the React applications successfully fetch and display data from the backend.
3.  **Global Preference Check:** Manually verify that every single line of code has an explanatory comment.

## Alternatives Considered
- **Pure Python (Flask/Django Templates):** While simpler for a Python learner, it lacks the modern feel of a React frontend. The proposed hybrid approach (Python backend + React frontend) provides the best of both worlds.
- **Serverless Functions:** Might be overkill for this stage of development and more complex to set up locally.
