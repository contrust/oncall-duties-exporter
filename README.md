# Oncall duties exporter
A custom prometheus exporter for the oncall app https://github.com/contrust/oncall, which allows to figure out if there's currently a person with a certain role in a team.
# Metrics format
duty{role=["primary" | "secondary"], team=team_name} [0.0, 1.0]
# Usage
```sh
python3 main.py [-h] [--https] [--update-retries-max-amount UPDATE_RETRIES_MAX_AMOUNT]
               [--update-retry-time-in-seconds UPDATE_RETRY_TIME_IN_SECONDS]
               [--requests-timeout-in-seconds REQUESTS_TIMEOUT_IN_SECONDS]
               [--metric-update-time-in-seconds METRIC_UPDATE_TIME_IN_SECONDS] [-v]
               port oncall-host
```
| Option | Description |
| --- | --- |
| port | The port of a prometheus client server |
| oncall-host | The host address of an oncall app (e.g., localhost:8080) |
| -h, --help | Show the help message |
| --https  | A flag for using a https scheme, http by default |
| --update-retries-max-amount UPDATE_RETRIES_MAX_AMOUNT | The number of times the app tries to get metrics again after a request error, 5 by default |
| --update-retry-time-in-seconds UPDATE_RETRY_TIME_IN_SECONDS | The time in seconds the app is sleeping before trying to get metrics again after a request error, 5.0 by default |
| --requests-timeout-in-seconds REQUESTS_TIMEOUT_IN_SECONDS | The timeout in seconds of a request to an oncall api, 5.0 by default. |
| --metric-update-time-in-seconds METRIC_UPDATE_TIME_IN_SECONDS | The time in seconds after the app is trying to update metrics, 3600.0 by default |
| -v | A flag for enabling a debug mode, false by default |
