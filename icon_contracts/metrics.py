from prometheus_client import Gauge
from icon_contracts.config import settings

class Metrics:
    def __init__(self):

        self.preps_created_python = Gauge(
            "contracts_created_python",
            "Num created.",
            ["network_name"],
        )

#
#     def set(self, metric, value):
#         metric = getattr(self, metric)
#         metric.labels(settings.NETWORK_NAME).set(value)
#
#
# if __name__ == '__main__':
#     from prometheus_client import start_http_server
#     from multiprocessing.pool import ThreadPool
#
#     metrics_pool = ThreadPool(1)
#
#     metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))
#     start_http_server(9401, "localhost")
#
#     m = Metrics()
#     m.set("preps_created_python")