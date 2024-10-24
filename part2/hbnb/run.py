import sys
import os

# Add the directory containing the app module to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app  # Import the create_app function from the app module

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
