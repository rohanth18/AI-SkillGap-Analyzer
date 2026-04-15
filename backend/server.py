from waitress import serve
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

if __name__ == "__main__":
    # Initialize database
    with app.app_context():
        db.create_all()
    
    print("Starting Waitress Server on http://127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)
