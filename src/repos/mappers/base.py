from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: Optional[type[DBModelType]] = None
    schema: Optional[type[SchemaType]] = None

    @classmethod
    def map_to_domain_entity(cls, data: DBModelType) -> SchemaType:
        if cls.schema is None:
            raise ValueError("Schema has not been set.")
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: SchemaType) -> DBModelType:
        if cls.db_model is None:
            raise ValueError("DB model has not been set.")
        return cls.db_model(**data.model_dump())
