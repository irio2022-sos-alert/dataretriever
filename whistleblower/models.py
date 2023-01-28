from sqlmodel import Field, SQLModel


class Service(SQLModel, table=True):
    __tablename__ = "service"
    id: int = Field(primary_key=True)
    name: str = Field(primary_key=True)
    domain: str 
    frequency: int
    alerting_window: int
    allowed_response_time: int
    email: str


class Responses(SQLModel, table=True):
    __tablename__ = "responses"
    service_id: int = Field(foreign_key="service.id", primary_key=True)
    timestamp: int
