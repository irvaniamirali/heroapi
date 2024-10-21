from uuid import uuid4
from base64 import urlsafe_b64encode


def generate_short_url():
    unique_id = uuid4()
    uuid_bytes = unique_id.bytes
    encoded = urlsafe_b64encode(uuid_bytes)
    short_url = encoded.decode("ascii").rstrip("=")
    return short_url[:6]
