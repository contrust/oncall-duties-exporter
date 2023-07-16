import logging
import sys
import time

import prometheus_client
import requests

from src.oncall.api.team_summary import get_team_summary
from src.oncall.api.teams import get_teams


def try_update_duty_metric(duty_metric: prometheus_client.metrics.Gauge,
                           oncall_host: str,
                           requests_timeout_in_seconds: float,
                           is_https: bool) -> bool:
    duty_metric.clear()
    try:
        response = get_teams(oncall_host, requests_timeout_in_seconds, is_https)
        response.raise_for_status()
        teams = response.json()
    except requests.exceptions.RequestException as e:
        logging.exception(e, exc_info=False)
        return False
    for team in teams:
        try:
            response = get_team_summary(oncall_host, team, requests_timeout_in_seconds, is_https)
            response.raise_for_status()
            team_summary = response.json()
        except requests.exceptions.RequestException as e:
            logging.exception(e, exc_info=False)
            return False
        current_team_summary = team_summary.get("current", None)
        if current_team_summary is not None:
            duty_metric.labels(team, "primary").set("primary" in current_team_summary)
            duty_metric.labels(team, "secondary").set("secondary" in current_team_summary)
    return True


def update_duty_metric(duty_metric: prometheus_client.metrics.Gauge,
                       oncall_host: str,
                       is_https: bool,
                       update_retries_max_amount: int,
                       update_retry_time_in_seconds: float,
                       requests_timeout_in_seconds: float):
    update_retries_amount = 0
    is_duty_metric_updated = False
    while update_retries_amount <= update_retries_max_amount:
        if update_retries_amount != 0:
            logging.debug(f"Sleeping for {update_retry_time_in_seconds} seconds before "
                          f"trying get the duty metric from {oncall_host} again, "
                          f"{update_retries_max_amount - update_retries_amount + 1} attempts remaining.")
            time.sleep(update_retry_time_in_seconds)
        is_duty_metric_updated = try_update_duty_metric(duty_metric, oncall_host, requests_timeout_in_seconds, is_https)
        if is_duty_metric_updated:
            break
        duty_metric.clear()
        update_retries_amount += 1
    logging.info(f"The duty metric was{' ' if is_duty_metric_updated else ' not '}updated from {oncall_host}.")
    return is_duty_metric_updated


def start_update_duty_metric_loop(duty_metric: prometheus_client.metrics.Gauge,
                                  oncall_host: str,
                                  is_https: bool,
                                  update_retries_max_amount: int,
                                  update_retry_time_in_seconds: float,
                                  requests_timeout_in_seconds: float,
                                  metric_update_time_in_seconds: float):
    while True:
        if not update_duty_metric(duty_metric, oncall_host, is_https, update_retries_max_amount,
                                  update_retry_time_in_seconds, requests_timeout_in_seconds):
            sys.exit("Exit: can not update the duty metric.")
        logging.debug(f"Sleeping for {metric_update_time_in_seconds} seconds before "
                      f"updating the duty metric from {oncall_host} again.")
        time.sleep(metric_update_time_in_seconds)
