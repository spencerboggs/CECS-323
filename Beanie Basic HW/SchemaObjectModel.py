import datetime
from beanie import Document
from pydantic import Field, ConfigDict, field_validator

class SchemaObject(Document):
    model_config = ConfigDict(extra='forbid')

    schemaObjectName: str = Field(alias='object_name')
    description: str = Field(alias='description')
    creationDate: datetime.date = Field(alias='creation_date')

    class Settings:
        name = 'schema_object'

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
        return f'Schema Object: {self.schemaObjectName}, Created on: {self.creationDate}'
