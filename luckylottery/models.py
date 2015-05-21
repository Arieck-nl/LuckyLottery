from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# Model for Ticket
class Ticket(Base):
    __tablename__ = 'ticket'
    uid = Column(Integer, primary_key=True)
    email = Column(Text)

    def __init__(self, email):
        self.email = email

