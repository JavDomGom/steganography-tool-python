from src import config


def get_bytes(msg: str) -> list:
    return [bin(byte)[2:].zfill(config.BITS_X_CHAR)
            for byte in bytearray(msg, 'utf-8')]
