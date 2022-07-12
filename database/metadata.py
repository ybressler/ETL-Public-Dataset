from sqlalchemy import MetaData
from sqlalchemy.sql.schema import DEFAULT_NAMING_CONVENTION
from database.connect import DEFAULT_SCHEMA

# Start metadata here and bind later
naming_convention = DEFAULT_NAMING_CONVENTION


metadata = MetaData(
    schema = DEFAULT_SCHEMA,
    naming_convention = naming_convention
)
