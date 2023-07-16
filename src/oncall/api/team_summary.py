import requests


def get_team_summary(host: str,
                     team: str,
                     timeout_in_seconds: float,
                     is_https: bool = False) -> requests.Response:
    url = f'{"https" if is_https else "http"}://{host}/api/v0/teams/{team}/summary'
    headers = {"Content-Type": "application/json"}
    return requests.get(url, headers=headers, timeout=timeout_in_seconds)
