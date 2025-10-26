#!/usr/bin/env python3
"""
Quick start script for Animal Endangerment Predictor API
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print("=" * 70)
    print("Animal Endangerment Predictor API")
    print("=" * 70)
    print(f"\nStarting API server on http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Interactive UI: http://{host}:{port}/redoc")
    print("\nExample request:")
    print('   curl -X POST "http://localhost:8000/risk" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"query": "Show tiger risk in India"}\'')
    print("\n" + "=" * 70 + "\n")
    
    # Check for API keys
    if not os.getenv("IUCN_TOKEN"):
        print("WARNING: IUCN_TOKEN not set in .env file")
        print("  Some species data will be unavailable")
        print("  Get token at: https://apiv3.iucnredlist.org/api/v3/token\n")
    else:
        print("IUCN Red List API token: CONFIGURED\n")
    
    if not os.getenv("FIRMS_KEY"):
        print("WARNING: FIRMS_KEY not set in .env file")
        print("  Fire detection data will be unavailable")
        print("  Get key at: https://firms.modaps.eosdis.nasa.gov/api/\n")
    
    if os.getenv("MAPBOX_TOKEN"):
        print("Mapbox token: CONFIGURED (map visualization enabled)\n")
    
    # Run server
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        app_dir="src"
    )

