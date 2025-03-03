from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from configparser import ConfigParser

"""ConfigParser is a tool native to Python that allows us to easily parse an initialization
file.  Putting the parameters for the connection string and the schema into a config.ini 
file makes it easy to change which PostgreSQL database we connect to without changing the 
code, and saves us from having to type all of that information into the application every
time that we run it."""
config = ConfigParser()
config.read('config.ini')  # the config.ini file has to be in the working directory.

schema = config['schema']['schema name']

# create an instance of Metadata and specify the schema name that we want to use.
# otherwise, this just defaults to the postgres schema of the database.
metadata_obj = MetaData(schema=schema)
"""Base is a thin wrapper on DeclarativeBase.  The only thing that we are adding
in our case is the declaration of the default schema that we will use for this
run of the application.  There are many other parameters that SQLAlchemy keeps in 
metadata, but they are not essential to our work."""
class Base(DeclarativeBase):
    """
    This Base class is just a wrapper for the DeclarativeBase class that we get from
    SQLAlchemy.  The only real benefit to this is that we're able to give SQLAlchemy
    the name of the default schema that we want for it to use.
    """
    metadata = metadata_obj

# Honestly, this could have been done in the main, but it seems better structure to
# do it here and not expose the main to the mechanics of getting the metadata object
# out of our newly minted Base class.
metadata = Base.metadata
