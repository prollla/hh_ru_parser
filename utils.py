import requests


def fetch_json(url, params=None):
    """Выполняет GET-запрос и возвращает JSON-ответ."""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
