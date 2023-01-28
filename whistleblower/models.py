# from sqlmodel import Field, SQLModel


# class Services(SQLModel, table=True):
#     __tablename__ = "services"
#     id: int = Field(primary_key=True)
#     name: str


# class Responses(SQLModel, table=True):
#     __tablename__ = "responses"
#     service_id: int = Field(foreign_key="services.id", primary_key=True)
#     time: float
#     positive: bool

from sqlmodel import Field, SQLModel


class Services(SQLModel, table=True):
    __tablename__ = "services"
    id: int = Field(primary_key=True)
    name: str


class Admins(SQLModel, table=True):
    __tablename__ = "admins"
    id: int = Field(primary_key=True)
    email: str


class Ownership(SQLModel, table=True):
    __tablename__ = "ownership"
    service_id: int = Field(foreign_key="services.id", primary_key=True)
    admin_id: int = Field(foreign_key="admins.id", primary_key=True)
    first_contact: bool


class Alerts(SQLModel, table=True):
    __tablename__ = "alerts"
    service_id: int = Field(foreign_key="services.id", primary_key=True)