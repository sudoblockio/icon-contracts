import argparse

# Protobuf generated class; resides at ./user_pb2.py
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import StringDeserializer

from icon_contracts.schemas import transaction_raw_pb2

def main():
    topic = 'transactions'

    protobuf_deserializer = ProtobufDeserializer(transaction_raw_pb2.TransactionRaw)
    string_deserializer = StringDeserializer('utf_8')

    consumer_conf = {'bootstrap.servers': 'localhost:29092',
                     'key.deserializer': string_deserializer,
                     'value.deserializer': protobuf_deserializer,
                     'group.id': 'foo',
                     'auto.offset.reset': "earliest"}

    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([topic])

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            user = msg.value()
            if user is not None:
                print("User record {}: name: {}\n"
                      "\tfavorite_number: {}\n"
                      "\tfavorite_color: {}\n"
                      .format(msg.key(), user.name,
                              user.favorite_color,
                              user.favorite_number))
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
