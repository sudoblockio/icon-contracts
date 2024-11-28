import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    NAME: str = "contracts"
    VERSION: str = "v0.2.6"  # x-release-please-version
    NETWORK_NAME: str = "mainnet"

    # Ports
    PORT: int = 8000
    HEALTH_PORT: int = 8080
    METRICS_PORT: int = 9400

    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/health"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/contracts/docs"

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: str = "GET,POST,HEAD,OPTIONS"
    CORS_ALLOW_HEADERS: str = ""
    CORS_EXPOSE_HEADERS: str = "x-total-count"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # Logging
    LOG_MSG_SKIP: int = 100000
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: str = "false"
    LOG_FILE_NAME: str = "contracts.log"
    LOG_FORMAT: str = "string"

    # ICON Nodes
    ICON_NODE_URL = "https://api.icon.community/api/v3"
    # ICON_NODE_URL: str = "https://berlin.net.solidwallet.io/api/v3"
    BACKUP_ICON_NODE_URL = "https://ctz.solidwallet.io/api/v3"

    COMMUNITY_API_ENDPOINT: str = "https://tracker.icon.community"

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    # SCHEMA_REGISTRY_URL: str = "http://localhost:8081"

    # KAFKA_GROUP_ID: str = "contracts"
    CONSUMER_IS_TAIL: bool = False
    JOB_ID: str = None
    CONSUMER_GROUP: str = "contracts"
    # Change this to "earliest" + CONSUMER_GROUP to trigger a manual backfill
    CONSUMER_AUTO_OFFSET_RESET: str = "latest"

    CONSUMER_TOPIC_BLOCKS: str = "blocks"

    PRODUCER_TOPIC_DLQ: str = "contracts-worker-dlq"
    PRODUCER_TOPIC_CONTRACTS: str = "contracts-processed"

    # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Contract S3 Upload
    CONTRACTS_S3_AWS_ACCESS_KEY_ID: str = None
    CONTRACTS_S3_AWS_SECRET_ACCESS_KEY: str = None
    CONTRACTS_S3_BUCKET: str = None

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    UNZIP_PYTHON_SOURCE_CODE: bool = False

    ENABLE_CONTRACT_VERIFICATION: bool = True
    # Using this setting could be confusing. Might just be easier to check against
    # a list of valid contracts on each network. Also list input would need delimination
    # CONTRACT_VERIFICATION_CONTRACT: list = []  # Blank to use default list
    # TODO: Default to True after dev to cleanup old contracts
    CONTRACT_VERIFICATION_CLEANUP: bool = False

    # This defaulting to the container path and is overrided in tests
    GRADLE_PATH: str = "/opt"

    # # Redis
    # REDIS_HOST: str = "redis"
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str = ""
    # REDIS_CHANNEL: str = "contracts"
    # REDIS_SENTINEL_CLIENT_MODE: bool = False
    # REDIS_SENTINEL_CLIENT_MASTER_NAME: str = "master"

    governance_address: str = "cx0000000000000000000000000000000000000000"
    one_address: str = "cx0000000000000000000000000000000000000001"

    class Config:
        case_sensitive = False


if os.environ.get("ENV_FILE", False):
    settings = Settings(_env_file=os.environ.get("ENV_FILE"))
else:
    settings = Settings()
