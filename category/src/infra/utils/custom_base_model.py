from pydantic import BaseModel, ConfigDict, model_validator, field_validator, field_serializer
from bson.objectid import ObjectId
from typing import TypeAlias, Literal, ClassVar, Any

db_stack_types: TypeAlias = Literal["no-sql", "sql"]

class CustomBaseModel(BaseModel):

    aliases: ClassVar[dict[str, str]] = {
        "id": "_id",
    }

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={
            ObjectId: str,
        },
    )

    @model_validator(mode="before")
    @classmethod
    def _apply_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for field_name, alias in cls.aliases.items():
                if alias in data:
                    data[field_name] = data.pop(alias)
        return data

    @field_validator("*", mode="before")
    @classmethod
    def _objectid_from_str(cls, value: Any) -> Any:
        if ObjectId.is_valid(value):
            return ObjectId(value)
        return value
    
    @field_serializer("*", when_used="json")
    def _serialize_objectid(self, value: Any) -> Any:
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def model_dump_for_db(
        self,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        exclude: set | None = None,
        mode: Literal["python", "json"] = "python",
    ) -> dict[str, Any]:
        
        exclude = (exclude or set()) | {"id", "_id"}
        
        return self.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude=exclude,
            mode=mode,
        )