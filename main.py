import logging
import argparse
import prometheus_client
from src.constants import DEFAULT_METRICS_UPDATE_TIME_IN_SECONDS, DEFAULT_UPDATE_RETRIES_MAX_AMOUNT, \
    DEFAULT_UPDATE_RETRY_TIME_IN_SECONDS, DEFAULT_REQUEST_TIMEOUT_IN_SECONDS, DEFAULT_LOGGING_FORMAT
from src.metrics.duty import start_update_duty_metric_loop
from src.prometheus_client.registry import unregister_default_metrics
from src.prometheus_client.metrics import DUTY


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'port',
        type=int,
        help='the port of a prometheus client server'
    )
    parser.add_argument(
        'oncall-host',
        type=str,
        help='the host address of an oncall app (e.g., localhost:8080)'
    )
    parser.add_argument(
        '--https',
        action='store_true',
        help='a flag for using a https scheme, http by default'
    )

    parser.add_argument(
        '--update-retries-max-amount',
        type=int,
        default=DEFAULT_UPDATE_RETRIES_MAX_AMOUNT,
        help='the number of times the app tries to get metrics again after a request error, '
             f'{DEFAULT_UPDATE_RETRIES_MAX_AMOUNT} by default.'
    )

    parser.add_argument(
        '--update-retry-time-in-seconds',
        type=float,
        default=DEFAULT_UPDATE_RETRY_TIME_IN_SECONDS,
        help='the time in seconds the app is sleeping before trying to get metrics again after a request error, '
             f'{DEFAULT_UPDATE_RETRY_TIME_IN_SECONDS} by default.'
    )

    parser.add_argument(
        '--requests-timeout-in-seconds',
        type=float,
        default=DEFAULT_REQUEST_TIMEOUT_IN_SECONDS,
        help='the timeout in seconds of a request to an oncall api, '
             f'{DEFAULT_REQUEST_TIMEOUT_IN_SECONDS} by default.'
    )

    parser.add_argument(
        '--metric-update-time-in-seconds',
        type=float,
        default=DEFAULT_METRICS_UPDATE_TIME_IN_SECONDS,
        help='the time in seconds after the app is trying to update metrics, '
             f'{DEFAULT_METRICS_UPDATE_TIME_IN_SECONDS} by default.'
    )

    parser.add_argument(
        '-v',
        action='store_true',
        help='a flag for enabling a debug mode, '
             'false by default.'
    )

    return parser.parse_args()


def main():
    args_dict = vars(parse_arguments())
    port = args_dict["port"]
    oncall_host = args_dict["oncall-host"]
    is_https = args_dict["https"]
    update_retries_max_amount = args_dict["update_retries_max_amount"]
    update_retry_time_in_seconds = args_dict["update_retry_time_in_seconds"]
    requests_timeout_in_seconds = args_dict["requests_timeout_in_seconds"]
    metric_update_time_in_seconds = args_dict["metric_update_time_in_seconds"]
    debug = args_dict["v"]
    logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=logging.DEBUG if debug else logging.INFO)
    unregister_default_metrics()
    prometheus_client.start_http_server(port)
    logging.info(f"Run prometheus client on port {port}.")
    start_update_duty_metric_loop(DUTY, oncall_host, is_https, update_retries_max_amount, update_retry_time_in_seconds,
                                  requests_timeout_in_seconds, metric_update_time_in_seconds)


if __name__ == "__main__":
    main()
