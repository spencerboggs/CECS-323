import datetime

from beanie import Document, Indexed, Link
from pydantic import Field, ConfigDict, AfterValidator, validator, field_validator

class SchemaModel(Document):
    model_config = ConfigDict(extra='forbid')
    schemaName: str = Field(alias='schema_name')
    description: str = Field(alias='description')
    creationDate: datetime.date = Field(alias='creation_date')

    class Settings:
        name = 'schemas'

    @field_validator("description", mode='before')
    def validate_description(cls, description: str) -> str:
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if len(description) <= 10:
            raise ValueError('Your description is too short')
        elif len(description) > 128:
            raise ValueError('Your description is too long')
        return description
    
    @field_validator("creationDate", mode='before')
    def validate_creationDate(cls, creationDate: datetime.date) -> datetime.date:
        if isinstance(creationDate, datetime.datetime):
            creationDate = creationDate.date()
        elif creationDate < datetime.date(1960, 1, 1):
            raise ValueError('Creation date cannot be earlier than 1960')
        elif creationDate > datetime.date.today():
            raise ValueError('Creation date cannot be in the future')
        return creationDate

    def __str__(self):
        return f'Schema: {self.schemaName}, Created on: {self.creationDate}'

