import os

import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app # Imports the function to integrate ADK with FastAPI

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__)) # Gets the current directory path

# Example session DB URL (e.g., SQLite)
SESSION_DB_URL = "sqlite:///./sessions.db" # Configures a local SQLite database for sessions (primarily for dev/testing)

# Example allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"] # Configures allowed origins for Cross-Origin Resource Sharing (CORS)

# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True # Flag to indicate if a web interface should be served by the ADK FastAPI integration

# Call the function to get the FastAPI app instance
# Ensure the agent directory name ('capital_agent') matches your agent folder - Note: This comment mentions 'capital_agent', but AGENT_DIR is used below
app: FastAPI = get_fast_api_app(
    agent_dir=AGENT_DIR, # Passes the directory where your agent's configuration and code are located
    session_db_url=SESSION_DB_URL, # Passes the session database URL
    allow_origins=ALLOWED_ORIGINS, # Passes the CORS allowed origins
    web=SERVE_WEB_INTERFACE, # Passes the web interface flag
)

# You can add more FastAPI routes or configurations below if needed
# Example:
# @app.get("/hello")
# async def read_root():
#     return {"Hello": "World"}

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))) # Runs the FastAPI app using uvicorn