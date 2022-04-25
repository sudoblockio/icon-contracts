from time import sleep
from typing import Any

from confluent_kafka import (
    Consumer,
    DeserializingConsumer,
    KafkaError,
    Message,
    Producer,
    SerializingProducer,
    TopicPartition,
)
from confluent_kafka.admin import AdminClient
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import (
    ProtobufDeserializer,
    ProtobufSerializer,
)
from confluent_kafka.serialization import (
    IntegerDeserializer,
    StringDeserializer,
    StringSerializer,
)
from loguru import logger
from pydantic import BaseModel

from icon_contracts.config import settings

# from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.schemas.block_etl_pb2 import BlockETL
from icon_contracts.schemas.contract_processed_pb2 import ContractProcessed


def get_current_offset(session):
    """
    For backfilling only, this function works with the init container to look up
    it's job_id so it can line that up with it's consumer group and offest so that
    we can backfill up to a given point and then kill the worker afterwards.
    """
    if settings.JOB_ID is None:
        return settings.CONSUMER_GROUP, None

    output = {}
    while True:
        logger.info(f"Getting kafka job with job_id = {settings.JOB_ID}")
        sql = f"select * from kafka_jobs WHERE job_id='{settings.JOB_ID}';"
        result = session.execute(sql).fetchall()
        session.commit()

        if len(result) == 0:
            logger.info(f"Did not find job_id={settings.JOB_ID} - sleeping")
            sleep(2)
            continue

        for r in result:
            # Keyed on tuple of topic, partition to look up the stop_offset
            output[(r[2], r[3])] = r[4]

        return r[1], output


from typing import Type


class Worker(BaseModel):
    name: str = None
    # schema_registry_url: str = settings.SCHEMA_REGISTRY_URL
    schema_registry_client: Any = None
    sleep_seconds: float = 0.25

    session: Any = None

    kafka_server: str = settings.KAFKA_BROKER_URL
    consumer_group: str = None
    auto_offset_reset: str = "earliest"

    topic: str = None

    consumer: Any = None
    json_producer: Any = None

    protobuf_producer: Any = None
    protobuf_serializer: Any = None

    block: Type[BlockETL] = None
    msg: Message = None

    consumer_schema: Any = None
    check_topics: bool = True

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.name is None:
            self.name = self.topic

        self.block = BlockETL()

        # self.consumer = DeserializingConsumer(
        #     {
        #         "bootstrap.servers": self.kafka_server,
        #         "group.id": self.consumer_group,
        #         "key.deserializer": StringDeserializer("utf_8"),
        #         # "key.deserializer": IntegerDeserializer(),
        #         "queued.max.messages.kbytes": "100MB",
        #         "value.deserializer": ProtobufDeserializer(
        #             message_type=BlockETL, conf={"use.deprecated.format": True}
        #         ),
        #         # Offset determined by worker type head (latest) or tail (earliest)
        #         "auto.offset.reset": self.auto_offset_reset,
        #     }
        # )

        self.consumer = Consumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": self.consumer_group,
                # "queued.max.messages.kbytes": "100MB",
                # Offset determined by worker type head (latest) or tail (earliest)
                "auto.offset.reset": self.auto_offset_reset,
            }
        )

        # # Producers
        # # Json producer for dead letter queues
        self.json_producer = Producer({"bootstrap.servers": self.kafka_server})
        #
        # self.schema_registry_client = SchemaRegistryClient({"url": settings.SCHEMA_REGISTRY_URL})
        #
        # self.protobuf_serializer = ProtobufSerializer(
        #     ContractProcessed,
        #     self.schema_registry_client,
        #     conf={
        #         "auto.register.schemas": True,
        #         "use.deprecated.format": True,
        #     },
        # )
        #
        # self.protobuf_producer = SerializingProducer(
        #     {
        #         "bootstrap.servers": self.kafka_server,
        #         "key.serializer": StringSerializer("utf_8"),
        #         "value.serializer": self.protobuf_serializer,
        #     }
        # )

        if self.check_topics:
            admin_client = AdminClient({"bootstrap.servers": self.kafka_server})
            topics = admin_client.list_topics().topics

            if self.topic and self.topic not in topics:
                # Used as bare producer as well
                raise RuntimeError(f"Topic {self.topic} not in {topics}")

        self.init()

    # @staticmethod
    # def deserialize(byte_message, proto_type):
    #     module_, class_ = proto_type.rsplit('.', 1)
    #     class_ = getattr(import_module(module_), class_)
    #     rv = class_()
    #     rv.ParseFromString(byte_message)
    #     return rv

    def produce_json(self, topic, key, value):
        try:
            # https://github.com/confluentinc/confluent-kafka-python/issues/137#issuecomment-282427382
            self.json_producer.produce(topic=topic, value=value, key=key)
            self.json_producer.poll(0)
        except BufferError:
            self.json_producer.poll(1)
            self.json_producer.produce(topic=topic, value=value, key=key)
        self.json_producer.flush()

    def produce_protobuf(self, topic, key, value):
        try:
            self.protobuf_producer.produce(topic=topic, value=value, key=key)
            self.protobuf_producer.poll(0)
        except BufferError:
            self.protobuf_producer.poll(1)
            self.protobuf_producer.produce(topic=topic, value=value, key=key)
        self.protobuf_producer.flush()

    def start(self):
        self.consumer.subscribe([self.topic])
        logger.info(f"Kafka consumer connected to consumer group = {settings.CONSUMER_GROUP}...")

        while True:
            # Poll for a message
            msg = self.consumer.poll(timeout=1)

            # If no new message, try again
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    err_msg = "{topic} {partition} reached end at offset {offset}".format(
                        topic=msg.topic(),
                        partition=msg.partition(),
                        offset=msg.auto_offset_reset(),
                    )
                    logger.error("Kafka consumer: " + err_msg)
                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    logger.error(
                        f"Kafka consumer: Kafka topic {msg.topic()} not ready. Restarting."
                    )
                elif msg.error():
                    logger.error("Kafka consumer: " + str(msg.error()))
                sleep(1)
                continue
            else:
                self.msg = msg
                self.block.ParseFromString(msg.value())
                # self.process(msg)
                self.process()

        # Flush the last of the messages
        self.json_producer.flush()

    def get_offset_per_partition(self):
        topic = self.consumer.list_topics(topic=self.topic)
        partitions = [
            TopicPartition(self.topic, partition)
            for partition in list(topic.topics[self.topic].partitions.keys())
        ]

        return self.consumer.position(partitions)

    def init(self):
        """Overridable process that runs on init."""
        pass

    def process(self):
        """Overridable process that processes each message."""
        pass
