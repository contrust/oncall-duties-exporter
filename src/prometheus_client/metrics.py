from prometheus_client import Gauge


DUTY = Gauge(name="duty",
             labelnames=["team", "role"],
             documentation="shows if a user with certain role in a team exists.")
