# wsgi.py
from app import app

if __name__ == "__main__":
    # Optional: fallback if someone runs `python wsgi.py`
    app.run()