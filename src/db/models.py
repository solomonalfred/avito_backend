from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, TIMESTAMP, DECIMAL, Boolean
from datetime import datetime


metadata = MetaData()


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("nickname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("role", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow)
)
