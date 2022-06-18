from os import getenv
from flask_sqlalchemy import SQLAlchemy

db = None

def get_session():
    return db.session

def init(app):
    global db

    uri = getenv("DATABASE_URL")

    # Hack that will fix the deprecated URI Heroku uses
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    db = SQLAlchemy(app)
    print("========================== DB INITITALIZED")
