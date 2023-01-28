from sqlmodel import Field, SQLModel


class Services(SQLModel, table=True):
    __tablename__ = "services"
    id: int = Field(primary_key=True)
    name: str


class Responses(SQLModel, table=True):
    __tablename__ = "responses"
    service_id: int = Field(foreign_key="services.id", primary_key=True)
    time: float
    positive: bool
