from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ["domain"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: str
    def __init__(self, domain: _Optional[str] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...
