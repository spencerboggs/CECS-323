import logging
from configparser import ConfigParser
import datetime

import pytest
from sqlalchemy.exc import IntegrityError, StatementError, DataError
from sqlalchemy.orm import sessionmaker

from Utilities import get_test_engine
from orm_base import metadata, Base
from SchemaModel import Schema
from SchemaObjectModel import SchemaObject

@pytest.fixture(scope='function')
def db_session():
    config = ConfigParser()
    config.read('config.ini')
    log_level = eval(config['logging']['level'])
    logging.basicConfig(level=log_level)
    logging.getLogger("sqlalchemy.engine").setLevel(log_level)
    logging.getLogger("sqlalchemy.pool").setLevel(log_level)
    engine = get_test_engine()
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    
def test_insert_SchemaObject(db_session):
    schema = Schema(schemaName="TestSchema", description="Test schema", creationDate=datetime.date(2025, 2, 20))
    db_session.add(schema)
    db_session.flush()

    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
    db_session.add(schema_object)
    db_session.flush()
    schema_count = db_session.query(SchemaObject).filter_by(schemaObjectName=schema_object.schemaObjectName).count()
    assert schema_count == 1

def test_bad_schemaName_SchemaObject(db_session):
    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
    with pytest.raises(IntegrityError) as IE:
        db_session.add(schema_object)
        db_session.flush()
    assert str(IE.value).find('insert or update on table "schema_objects" violates foreign key constraint "schema_object_schema_fk_01"') > -1

def test_bad_name_type_SchemaObject(db_session):
    with pytest.raises(TypeError) as TE:
        schema_object = SchemaObject(schemaObjectName=123, description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
        db_session.add(schema_object)
        db_session.flush()
    assert str(TE.value).find("schemaObjectName must be a string") > -1

def test_bad_description_type_SchemaObject(db_session):
    with pytest.raises(TypeError) as TE:
        schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description=123, creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
        db_session.add(schema_object)
        db_session.flush()
    assert str(TE.value).find("description must be a string") > -1

def test_bad_creationDate_type_SchemaObject(db_session):
    with pytest.raises(ValueError) as VE:
        schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate="2025-02-20", schemaName="TestSchema")
        db_session.add(schema_object)
        db_session.flush()
    assert str(VE.value).find("Your creation date isn't formatted correctly") > -1

def test_tooLongString_SchemaObject(db_session):
    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="x" * 129, creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
    with pytest.raises(DataError) as DE:
        db_session.add(schema_object)
        db_session.flush()
    assert str(DE.value).find("value too long for type character varying") > -1

def test_insert_into_non_existent_Schema(db_session):
    with pytest.raises(IntegrityError) as IE:
        schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
        db_session.add(schema_object)
        db_session.flush()
    assert str(IE.value).find('violates foreign key constraint "schema_object_schema_fk_01"') > -1

def test_duplicate_SchemaObject_in_same_Schema(db_session):
    schema = Schema(schemaName="TestSchema", description="Test schema", creationDate=datetime.date(2025, 2, 20))
    db_session.add(schema)
    db_session.flush()

    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
    db_session.add(schema_object)
    db_session.flush()

    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
    db_session.add(schema_object)
    with pytest.raises(IntegrityError) as IE:
        db_session.flush()
    assert str(IE.value).find('duplicate key value violates unique constraint "schema_object_pk"') > -1

def test_duplicate_SchemaObject_in_different_Schema(db_session):
    schema = Schema(schemaName="TestSchema", description="Test schema", creationDate=datetime.date(2025, 2, 20))
    db_session.add(schema)
    db_session.flush()

    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
    db_session.add(schema_object)
    db_session.flush()

    schema = Schema(schemaName="TestSchema2", description="Test schema", creationDate=datetime.date(2025, 2, 20))
    db_session.add(schema)
    db_session.flush()

    schema_object = SchemaObject(schemaObjectName="TestSchemaObject", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema2")
    db_session.add(schema_object)
    db_session.flush()
    schema_count = db_session.query(SchemaObject).filter_by(schemaObjectName=schema_object.schemaObjectName).count()
    assert schema_count == 2

def test_SchemaObject_bad_length_name(db_session):
    with pytest.raises(ValueError) as VE:
        schema_object = SchemaObject(schemaObjectName="Test", description="Test schema object", creationDate=datetime.date(2025, 2, 20), schemaName="TestSchema")
        db_session.add(schema_object)
        db_session.flush()
    assert str(VE.value).find("schemaObjectName must be between 5 and 64 characters") > -1
