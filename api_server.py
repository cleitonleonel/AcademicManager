"""
API server entry point.

Run with:
    python api_server.py

Or directly with uvicorn:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import uvicorn

if __name__ == "__main__":
    print("🚀 Academic Manager — API Server")
    print("📚 Documentação (Swagger): http://localhost:8000/docs")
    print("📖 ReDoc:                  http://localhost:8000/redoc")
    print("🌐 Frontend:               http://localhost:8000/")
    print()

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
