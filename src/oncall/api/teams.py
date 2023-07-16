import requests


def get_teams(host: str,
              timeout_in_seconds: float,
              is_https: bool = False) -> requests.Response:
    url = f'{"https" if is_https else "http"}://{host}/api/v0/teams'
    headers = {"Content-Type": "application/json"}
    return requests.get(url, headers=headers, timeout=timeout_in_seconds)
