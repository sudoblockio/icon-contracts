import ast

from loguru import logger


def sink(message):
    record = message.record
    if "deserialize" in record["extra"]:
        subset = {
            "timestamp": record["time"].timestamp(),
            "message": ast.literal_eval(record["message"]),
        }
    else:
        subset = {
            "timestamp": record["time"].timestamp(),
            "message": record["message"],
        }

    print(subset)


logger.remove()
logger.add(sink, enqueue=True)
