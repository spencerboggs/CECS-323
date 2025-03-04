import pytest
import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

from SchemaModel import SchemaModel

def get_SchemaModel():
    return {
        'schema_name': 'TestSchema',
        'description': 'A valid schema description.',
        'creation_date': datetime.date(2024, 2, 20)
    }

@pytest.fixture
async def init(event_loop):
    client = AsyncIOMotorClient("mongodb://localhost:27017/?directConnection=true&replicaSet=rs0&w=majority")
    db = client.get_database("BeanieTest")
    await init_beanie(database=db, document_models=[SchemaModel])
    return client

@pytest.mark.asyncio
async def test_insert_SchemaModel(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            schema_data = get_SchemaModel()
            schema = SchemaModel(**schema_data)
            await schema.insert(session=session)
            
            schemas = await SchemaModel.find(
                SchemaModel.schemaName == schema.schemaName,
                session=session
            ).to_list()
            
            assert len(schemas) == 1
            await schema.delete(session=session)

@pytest.mark.asyncio
async def test_bad_name_type_SchemaModel(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(ValidationError):
                schema_data = get_SchemaModel()
                schema_data['schemaName'] = 123
                schema = SchemaModel(**schema_data)
                await schema.insert(session=session)

@pytest.mark.asyncio
async def test_bad_description_type_SchemaModel(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(TypeError):
                schema_data = get_SchemaModel()
                schema_data['description'] = 123
                schema = SchemaModel(**schema_data)
                await schema.insert(session=session)

@pytest.mark.asyncio
async def test_bad_creationDate_type_SchemaModel(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(ValidationError) as exc_info:
                schema_data = get_SchemaModel()
                schema_data['creationDate'] = "2025-02-20"
                schema = SchemaModel(**schema_data)
                await schema.insert(session=session)

@pytest.mark.asyncio
async def test_tooLongString_SchemaModel(init):
    new_client = await init
    async with await new_client.start_session() as session:
        async with session.start_transaction():
            with pytest.raises(ValidationError):
                schema_data = get_SchemaModel()
                schema_data['description'] = 'A' * 129
                schema = SchemaModel(**schema_data)
                await schema.insert(session=session)
