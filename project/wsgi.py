from app import app

# Gunicorn entrypoint: `gunicorn wsgi:app`
if __name__ == "__main__":
    app.run()
