import uuid
import hashlib


def generate_uuid(input_str: str) -> uuid.UUID:
    # Convert the string to bytes if it's not already
    input_str = input_str if isinstance(input_str, bytes) else input_str.encode("utf-8")

    # Create a MD5 hash of the input string
    hash_object = hashlib.md5(input_str)
    hash_hex = hash_object.hexdigest()

    generated_uuid = uuid.UUID(hash_hex)

    return str(generated_uuid)
