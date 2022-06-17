from ast import Subscript
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null, text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, server_default='TRUE')
    Subscription_package = Column(String, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    tenent_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    subscription_package = Column(TIMESTAMP(timezone=True),
                                  nullable=False,
                                  server_default=text('now()'))
