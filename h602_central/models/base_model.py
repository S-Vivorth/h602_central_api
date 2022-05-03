from sqlalchemy import *
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from datetime import datetime



@as_declarative()
class base:
    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def is_active(self):
        return Column(Boolean, default=True)

    @declared_attr
    def created_date(self):
        return Column(DateTime, default=datetime.now)

    @declared_attr
    def updated_date(self):
        # trace both update and insert
        return Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def updated_by(self):
        return Column(String(200))

    @declared_attr
    def created_by(self):
        return Column(String(200))
