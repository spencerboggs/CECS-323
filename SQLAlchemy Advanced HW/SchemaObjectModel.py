import datetime
from sqlalchemy import String, Date, Integer, DECIMAL, PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from orm_base import Base
from SchemaModel import Schema

class SchemaObject(Base):
    __tablename__ = 'schema_objects'
    
    schemaName: Mapped[str] = mapped_column('schema_name', String(64), nullable=False)
    schemaObjectName: Mapped[str] = mapped_column('object_name', String(64),
                                                  CheckConstraint("LENGTH(object_name) >= 5 AND LENGTH(object_name) <= 64", name='schema_object_name_length'),
                                                  nullable=False)
    description: Mapped[str] = mapped_column('description', String(128), 
                                             CheckConstraint("LENGTH(description) >= 10 AND LENGTH(description) <= 128", name='schema_object_description_length'),
                                             nullable=False)
    creationDate: Mapped[datetime.date] = mapped_column('creation_date', Date, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('schema_name', 'object_name', name="schema_object_pk"),
        ForeignKeyConstraint(['schema_name'], ['schemas.name'], name='schema_object_schema_fk_01'),
    )

    @validates("schemaObjectName")
    def validate_schemaObjectName(self, key, schemaObjectName):
        if not isinstance(schemaObjectName, str):
            raise TypeError("schemaObjectName must be a string")
        if len(schemaObjectName) < 5 or len(schemaObjectName) > 64:
            raise ValueError("schemaObjectName must be between 5 and 64 characters")
        return schemaObjectName

    @validates("description")
    def validate_description(self, key, description: str):
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        elif  len(description) < 10:
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

    def __init__(self, schemaObjectName: str, description: str, creationDate: datetime.date, schemaName: str, **kwargs):
        super().__init__(**kwargs)
        self.schemaObjectName = schemaObjectName
        self.description = description
        self.creationDate = creationDate
        self.schemaName = schemaName

    def __str__(self):
        return f'Schema Object: {self.schemaObjectName}, Created on: {self.creationDate}'
