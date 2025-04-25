from src import create_app
import os


if __name__ == "__main__":
    app = create_app()
    debug_mode = os.getenv("APP_ENV") == "development"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
