import logging
import datetime
import pytest
from pydantic import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from SchemaObjectModel import SchemaObject

def get_SchemaObject_data():
    return {
        'object_name': 'TestSchemaObject',
        'description': 'Test schema object',
        'creation_date': datetime.date(2025, 2, 20)
    }

@pytest.fixture(scope='function')
async def init(event_loop):
    client = AsyncIOMotorClient("mongodb://localhost:27017/?directConnection=true&replicaSet=rs0&w=majority")
    db = client.get_database("BeanieTest")
    await init_beanie(database=db, document_models=[SchemaObject])
    return client

@pytest.mark.asyncio
async def test_insert_SchemaObject(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            schema_data = get_SchemaObject_data()
            schema = SchemaObject(**schema_data)
            await schema.insert(session=session)
            
            schemas = await SchemaObject.find(
                SchemaObject.schemaObjectName == schema.schemaObjectName,
                session=session
            ).to_list()
            
            assert len(schemas) == 1
            await schema.delete(session=session)

@pytest.mark.asyncio
async def test_bad_name_type_SchemaObject(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(ValidationError):
                schema_data = get_SchemaObject_data()
                schema_data['schemaObjectName'] = 123
                schema = SchemaObject(**schema_data)
                await schema.insert(session=session)

@pytest.mark.asyncio
async def test_bad_description_type_SchemaObject(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(TypeError):
                schema_data = get_SchemaObject_data()
                schema_data['description'] = 123
                schema = SchemaObject(**schema_data)
                await schema.insert(session=session)

@pytest.mark.asyncio
async def test_bad_creationDate_type_SchemaObject(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(ValidationError) as exc_info:
                schema_data = get_SchemaObject_data()
                schema_data['creationDate'] = "2025-02-20"
                schema = SchemaObject(**schema_data)
                await schema.insert(session=session)

@pytest.mark.asyncio
async def test_tooLongString_SchemaObject(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(ValidationError):
                schema_data = get_SchemaObject_data()
                schema_data['description'] = 'A' * 129
                schema = SchemaObject(**schema_data)
                await schema.insert(session=session)
