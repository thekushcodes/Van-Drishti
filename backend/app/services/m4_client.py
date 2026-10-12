import requests

from app.config import settings


class M4Client:
    def __init__(self):
        self.base_url = settings.m4_url.rstrip("/")

    def create_intelligence_run(self, payload: dict):
        url = f"{self.base_url}/api/v1/intelligence/runs"

        response = requests.post(
            url,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        return response.json()