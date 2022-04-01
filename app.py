import json
import os
from urllib.parse import urlencode

import requests
from flask import Flask, redirect, request, Response, jsonify, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# TODO: resolve circular imports through refactor
from models import User

def read_secrets(secret_path):
    try:
        with open(secret_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Secret not found in {secret_path}")


def create_app() -> Flask:
    app = Flask(__name__, template_folder='templates')
    secret_config = read_secrets(".secrets/strava-secrets.json")
    app.config.update(secret_config)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


app = create_app()
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    exists = db.session.query(User).filter_by(user_id=app.config["STRAVA_CLIENT_ID"]).first() is not None

    if exists:
        return "USER LOGGED IN"
    return render_template("home.html")


@app.route("/auth", methods=["GET"])
def strava_authorize():
    params = {
        "client_id": app.config["STRAVA_CLIENT_ID"],
        "response_type": "code",
        "redirect_uri": app.config["REDIRECT_URI"],
        "scope": "activity:read_all",
    }
    return redirect(f"https://www.strava.com/oauth/authorize?{urlencode(params)}")


def exchange_token(code):
    strava_request = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': app.config["STRAVA_CLIENT_ID"],
            'client_secret': app.config["STRAVA_CLIENT_SECRET"],
            'code': code,
            'grant_type': 'authorization_code'
        }
    )

    response = strava_request.json()
    # TODO: separate out into sep func with dict unpacking of athlete
    user = User(
        user_id = app.config["STRAVA_CLIENT_ID"],
        username = response["athlete"]["username"],
        firstname = response["athlete"]["firstname"],
        lastname = response["athlete"]["lastname"],
        sex = response["athlete"]["sex"],
        city = response["athlete"]["city"],
        country = response["athlete"]["country"],
        profile = response["athlete"]["profile"],
        weight = response["athlete"]["weight"],

        access_token = response["access_token"],
        refresh_token = response["refresh_token"],
        expires_at = response["expires_at"]
    )
    db.session.add(user)
    db.session.commit()

    #return jsonify(strava_request.json())
    return redirect(url_for("home"))


@app.route("/token")
def user_token_exchange():
    """Receive the user code and query Strava to get the final access token."""
    code = request.args.get('code')
    if not code:
        return Response('Error: Missing code param', status=400)
    return exchange_token(code)

