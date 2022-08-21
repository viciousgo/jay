import os
from hmac import new
from typing import Union
from hashlib import sha1
from base64 import b64encode


def device_id(data: bytes = None) -> str:
    if isinstance(data, str): data = bytes(data, 'utf-8')
    identifier = bytes.fromhex("42") + (data or os.urandom(20))
    mac = new(bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F"), identifier, sha1)
    return f"{identifier.hex()}{mac.hexdigest()}".upper()


def signature(data: Union[str, bytes]) -> str:
    data = data if isinstance(data, bytes) else data.encode("utf-8")
    return b64encode(bytes.fromhex("42") + new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), data, sha1).digest()).decode("utf-8")

def decode_sid(sid: str) -> dict:
    return json.loads(urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])


def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]

def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]

def sid_created_time(SID: str) -> str: return decode_sid(SID)["5"]

def sid_to_client_type(SID: str) -> str: return decode_sid(SID)["6"]
