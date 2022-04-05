from prometheus_client import Gauge

from icon_contracts.config import settings


class Metrics:
    def __init__(self):

        self.contracts_created_python = Gauge(
            "contracts_created_python",
            "Num created.",
        )

        self.contracts_updated_python = Gauge(
            "contracts_updated_python",
            "Num updated.",
        )

        self.block_height = Gauge(
            "max_block_number_transactions_raw",
            "The block height",
        )
