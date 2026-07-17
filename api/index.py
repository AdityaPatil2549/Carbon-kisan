"""
Vercel serverless entry point for CarbonKisan FastAPI backend.
This file is the bridge between Vercel's Python runtime and our FastAPI app.
"""
import sys
import os

# Add the backend directory to Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app

# Vercel expects the ASGI app to be named `app`
# FastAPI is already ASGI-compatible, so this works directly
