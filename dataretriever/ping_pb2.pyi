from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DrStatus(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ["domain"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: str
    def __init__(self, domain: _Optional[str] = ...) -> None: ...

class PingStatus(_message.Message):
    __slots__ = ["domain", "okay", "time"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    domain: str
    okay: bool
    time: float
    def __init__(self, domain: _Optional[str] = ..., time: _Optional[float] = ..., okay: bool = ...) -> None: ...

class WbStatus(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...
