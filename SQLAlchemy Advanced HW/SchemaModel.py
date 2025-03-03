import datetime
from typing import List
from sqlalchemy import String, Date, Integer, DECIMAL, PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from orm_base import Base

class Schema(Base):
    __tablename__ = 'schemas'
    
    schemaName: Mapped[str] = mapped_column('name', String(64),
                                            CheckConstraint("LENGTH(name) >= 5 AND LENGTH(name) <= 64", name='schema_name_length'),
                                            nullable=False)
    description: Mapped[str] = mapped_column('description', String(128),
                                             CheckConstraint("LENGTH(description) >= 10 AND LENGTH(description) <= 128", name='schema_description_length'), 
                                             nullable=False)
    creationDate: Mapped[datetime.date] = mapped_column('creation_date', Date, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(schemaName, name="schema_pk"),
    )
    
    @validates("schemaName")
    def validate_schemaName(self, key, schemaName):
        if not isinstance(schemaName, str):
            raise TypeError("schemaName must be a string")
        if len(schemaName) < 5 or len(schemaName) > 64:
            raise ValueError("schemaName must be between 5 and 64 characters")
        return schemaName

    @validates("description")
    def validate_description(self, key, description):
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        elif len(description) <= 10:
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
