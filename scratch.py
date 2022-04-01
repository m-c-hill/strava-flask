import json
import os
from pprint import pprint

import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def main():
    with open(".secrets/strava-secrets.json") as f:
        credentials = json.load(f)

    # Get authorization code from the auth endpoint
    CLIENT_ID = credentials["client_id"]
    REDIRECT_URI = "http://localhost"
    RESPONSE_TYPE = "code"
    SCOPE = "activity:read"
    headers = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": RESPONSE_TYPE,
        "scope": SCOPE,
    }

    # "Authorization": f"Bearer {token}"}

    response = requests.post(
        f"https://www.strava.com/api/v3/authorize", headers=headers
    )
    breakpoint()
    token = credentials["access_token"]

    # Athlete
    print("Request athlete id: 79857")
    get_response("athlete", headers)

    # TODO: request read_all as scope for authentication

    # Athlete Zones
    print("Getting athlete zones...")
    get_response("athlete/zones", headers)

    # Activities
    # activity_id = 6903475957
    # print(f"Request activity id: {activity_id}")
    # get_response(f"activities/{activity_id}", headers)


def get_response(endpoint: str, headers: dict) -> None:
    response = requests.get(
        f"https://www.strava.com/api/v3/{endpoint}", headers=headers
    )
    response.raise_for_status()
    response = response.json()
    pprint(response)
    print("\n")


if __name__ == "__main__":
    main()
