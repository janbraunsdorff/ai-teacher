from datetime import datetime


def convert_timestamp(timestamo: int):
    return datetime.utcfromtimestamp(timestamo / 10000).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
