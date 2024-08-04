from typing import Any

from pydantic import BaseModel, ValidationError, model_validator


class PatchModel(BaseModel):
    @classmethod
    def _raise_on_empty_data(cls, values: dict[str, Any]) -> None:
        """Check if data is empty"""
        if not values:
            raise ValidationError('Patch model cannot be empty')

    @model_validator(mode="before")
    @classmethod
    def validate(cls, values: Any) -> Any:
        """Validate user update data"""

        if isinstance(values, dict):
            cls._raise_on_empty_data(values)

        return values
