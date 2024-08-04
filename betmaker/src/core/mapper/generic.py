
from typing import TypeVar, Generic, Any

from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

from .base import AbstractMapper


S = TypeVar('S', bound=BaseModel)
M = TypeVar('M', bound=DeclarativeBase)


class SchemaToDatabaseMapper(AbstractMapper, Generic[M, S]):
    """
    A mapper class to map data between a Pydantic schema model and a SQLAlchemy database model.

    This class provides functionality to transform and transfer data from a Pydantic model
    to a SQLAlchemy model, allowing for optional custom key mapping.

    :param custom_mapping: An optional dictionary that defines custom mappings
                           between schema field names and database field names.
                           For example, {'schema_field': 'db_field'} will map
                           'schema_field' in the schema model to 'db_field' in
                           the database model.
    """

    def __init__(self, custom_mapping: dict[str, str] | None = None) -> None:
        """
        Initializes the SchemaToDatabaseMapper with an optional custom mapping.

        :param custom_mapping: An optional dictionary mapping schema field names
                               to database field names. If None, no custom mapping
                               is applied.
        """
        self.custom_mapping: dict[str, str] | None = custom_mapping

    def _get_real_key(self, k: str) -> str:
        """
        Retrieves the corresponding database field name for a given schema field name.

        This function uses the custom mapping dictionary to translate schema field names
        to their corresponding database field names. If no custom mapping exists for the
        given field name, the original field name is returned.

        :param k: The field name in the schema model.
        :return: The corresponding field name in the database model.
        :raises ValueError: If the provided field name does not have a corresponding entry
                            in the custom mapping dictionary.
        """
        if not self.custom_mapping:
            return k

        if k not in self.custom_mapping:
            raise ValueError(f'Custom mapping in SchemaToDatabaseMapper has not custom key for key={k}')

        return self.custom_mapping[k]

    def map(
        self,
        first: S,
        second: M,
        exclude: set[str] | None = None,
        exclude_unset: bool = False,
    ) -> M:
        """
        Maps fields from a Pydantic schema model to a SQLAlchemy database model.

        This method takes data from a Pydantic model (`first`) and maps it onto an existing
        SQLAlchemy model (`second`). The mapping respects the custom mapping dictionary
        and can optionally exclude specified fields.

        :param first: The Pydantic schema model to map data from.
        :param second: The SQLAlchemy model to map data to. This model will be updated
                       with the values from the schema model.
        :param exclude: A set of field names to exclude from the mapping process. If None,
                        no fields are excluded.
        :param exclude_unset: A boolean flag indicating whether to exclude fields from the
                              mapping that are unset (i.e., fields with default values that
                              have not been explicitly assigned).
        :return: The updated SQLAlchemy model with the mapped data.
        :raises ValueError: If a field in the schema model cannot be mapped to a corresponding
                            field in the database model due to missing attributes or mapping keys.
        """
        data: dict[str, Any] = first.model_dump(exclude=exclude, exclude_unset=exclude_unset)

        for k, v in data.items():
            # NOTE: if custom_mapping is unset, real_key = original key
            _real_key = self._get_real_key(k)

            if not hasattr(second, _real_key):
                raise ValueError(f'Key key={_real_key} has not mapping for {type(second)} in second!')

            setattr(second, _real_key, v)

        return second
