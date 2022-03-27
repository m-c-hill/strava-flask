import json

import requests


def main():
    with open(".secrets/strava-secrets.json") as f:
        credentials = json.load(f)
    breakpoint()
    token = credentials["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"https://www.strava.com/api/v3/athlete/activities", headers=headers
    )

    r.raise_for_status()


if __name__ == "__main__":
    main()
