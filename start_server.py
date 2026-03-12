"""
Quick start script for the FastAPI server
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting MedPredict AI Backend Server")
    print("=" * 60)
    print("\nServer will be available at: http://localhost:8008")
    print("API Documentation: http://localhost:8008/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8008,
        reload=True
    )

