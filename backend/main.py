from src import create_app
from src.db import initialize_db, close_db

app = create_app()

initialize_db()


@app.teardown_appcontext
def teardown_db(exception):
    close_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
