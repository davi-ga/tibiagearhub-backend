import requests


class TibiaDataAPI:
    def __init__(self) -> None:
        self.url = "https://api.tibiadata.com/v5/"

    def _get(self, path: str) -> dict | None:
        response = requests.get(f"{self.url}{path}")

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()

    def get_creatures(self) -> dict | None:
        return self._get("creatures/")

    def get_especific_creature(self, race: str) -> dict | None:
        return self._get(f"creatures/{race}")
