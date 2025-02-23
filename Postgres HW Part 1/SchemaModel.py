import datetime
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import PrimaryKeyConstraint
from orm_base import Base

class Schema(Base):
    __tablename__ = 'schema'
    
    schemaName: Mapped[str] = mapped_column('name', String(64), nullable=False)
    description: Mapped[str] = mapped_column('description', String(128), nullable=False)
    creationDate: Mapped[datetime.date] = mapped_column('creation_date', Date, nullable=False)

    PrimaryKeyConstraint(schemaName, name="schema_pk")

    @validates("description")
    def validate_description(self, key, description):
        if isinstance(description, str) and len(description) <= 10:
            raise ValueError("Your description is too short")
        return description

    @validates("creationDate")
    def validate_creationDate(self, key, creationDate: datetime.date):
        if not isinstance(creationDate, datetime.date):
            raise ValueError("Your creation date isn't formatted correctly")
        elif creationDate < datetime.date(1960, 1, 1):
            raise ValueError('Creation date cannot be earlier than 1960')
        elif creationDate > datetime.date.today():
            raise ValueError('Creation date cannot be in the future')
        return creationDate

    def __init__(self, schemaName: str, description: str, creationDate: datetime.date, **kwargs):
        super().__init__(**kwargs)
        self.schemaName = schemaName
        self.description = description
        self.creationDate = creationDate

    def __str__(self):
        return f'Schema: {self.schemaName}, Created on: {self.creationDate}'

