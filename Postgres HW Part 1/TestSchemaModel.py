import logging
from configparser import ConfigParser
import datetime

import pytest
from sqlalchemy.exc import IntegrityError, StatementError, DataError
from sqlalchemy.orm import sessionmaker

from Utilities import get_test_engine
from orm_base import metadata, Base
from SchemaModel import Schema

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

def test_insert_Schema(db_session):
    schema = Schema(schemaName="TestSchema", description="Test schema", creationDate=datetime.date(2025, 2, 20))
    db_session.add(schema)
    db_session.flush()
    schema_count = db_session.query(Schema).filter_by(schemaName=schema.schemaName).count()
    assert schema_count == 1

def test_bad_name_type_Schema(db_session):
    schema = Schema(schemaName=123, description="Test schema", creationDate=datetime.date(2025, 2, 20))
    try:
        db_session.add(schema)
        db_session.flush()
    except DataError:
        assert True
    
def test_bad_description_type_Schema(db_session):
    schema = Schema(schemaName="TestSchema", description=123, creationDate=datetime.date(2025, 2, 20))
    try:
        db_session.add(schema)
        db_session.flush()
    except DataError:
        assert True

def test_bad_creationDate_type_Schema(db_session):
    with pytest.raises(ValueError) as VE:
        schema = Schema(schemaName="TestSchema", description="Test schema", creationDate="2025-02-20")
        db_session.add(schema)
        db_session.flush()
    assert str(VE.value).find("Your creation date isn't formatted correctly") > -1

def test_tooLongString_Schema(db_session):
    schema = Schema(schemaName="TestSchema", description="A" * 129, creationDate=datetime.date(2025, 2, 20))
    with pytest.raises(DataError) as DE:
        db_session.add(schema)
        db_session.flush()
    assert str(DE.value).find('value too long for type character') > -1

