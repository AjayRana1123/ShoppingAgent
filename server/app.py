import sys
import os

# Allow imports from repo root (env.py, dataset.json, etc.)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: F401 - re-export the FastAPI app
import uvicorn


def start():
    """Entry point for the server (used by pyproject.toml scripts)."""
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 7860)),
        reload=False,
    )


if __name__ == "__main__":
    start()
