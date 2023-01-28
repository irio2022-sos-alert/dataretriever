from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AlertRequest(_message.Message):
    __slots__ = ["serviceId"]
    SERVICEID_FIELD_NUMBER: _ClassVar[int]
    serviceId: int
    def __init__(self, serviceId: _Optional[int] = ...) -> None: ...

class DrStatus(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ["domain", "service_id"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    domain: str
    service_id: int
    def __init__(self, service_id: _Optional[int] = ..., domain: _Optional[str] = ...) -> None: ...

class PingStatus(_message.Message):
    __slots__ = ["okay", "service_id", "timestamp"]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    okay: bool
    service_id: int
    timestamp: float
    def __init__(self, service_id: _Optional[int] = ..., timestamp: _Optional[float] = ..., okay: bool = ...) -> None: ...

class ReceiptConfirmation(_message.Message):
    __slots__ = ["serviceId"]
    SERVICEID_FIELD_NUMBER: _ClassVar[int]
    serviceId: int
    def __init__(self, serviceId: _Optional[int] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...

class WbStatus(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...
