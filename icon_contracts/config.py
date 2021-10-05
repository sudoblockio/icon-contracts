from pydantic import BaseSettings


class Settings(BaseSettings):

    name: str = "contracts"
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
    DOCS_PREFIX: str = "/api/v1/docs"

    CORS_ALLOW_ORIGINS: str = "*"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: str = "false"
    LOG_FILE_NAME: str = "contracts.log"
    LOG_FORMAT: str = "string"

    # ICON Nodes
    ICON_NODE_URL = "https://icon.geometry-dev.net/api/v3"
    BACKUP_ICON_NODE_URL = "http://34.218.244.40:9000/api/v3"

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"

    KAFKA_GROUP_ID: str = "contracts-service"

    # Topics
    CONSUMER_GROUP_HEAD: str = "contracts-head"
    CONSUMER_GROUP_TAIL: str = "contracts-tail"

    CONSUMER_TOPIC_BLOCKS: str = "blocks"
    CONSUMER_TOPIC_TRANSACTIONS: str = "transactions"
    CONSUMER_TOPIC_LOGS: str = "logs"

    PRODUCER_TOPIC_DLQ: str = "contracts-worker-dlq"
    PRODUCER_TOPIC_TOKENS: str = "tokens-contracts"

    # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Contract S3 Upload
    CONTRACTS_S3_AWS_ACCESS_KEY_ID: str = None
    CONTRACTS_S3_AWS_SECRET_ACCESS_KEY: str = None
    CONTRACTS_S3_BUCKET: str = "icon-explorer-dev"

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    UNZIP_PYTHON_SOURCE_CODE: bool = False

    # # Redis
    # REDIS_HOST: str = "redis"
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str = ""
    # REDIS_CHANNEL: str = "contracts"
    # REDIS_SENTINEL_CLIENT_MODE: bool = False
    # REDIS_SENTINEL_CLIENT_MASTER_NAME: str = "master"

    _governance_address: str = "cx0000000000000000000000000000000000000000"
    one_address: str = "cx0000000000000000000000000000000000000001"

    class Config:
        case_sensitive = False


settings = Settings()
