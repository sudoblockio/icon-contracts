from prometheus_client import Gauge


class Metrics:
    def __init__(self):

        self.preps_created = Gauge(
            "contracts_preps_created",
            "Num created.",
            ["network_name"],
        )
