from enum import Enum


__all__ = [
    "PydanticStringEnum",
]


class PydanticStringEnum(str, Enum):
    """Version of String enum which can be validated through Pydantic

    by str as name or value of enum fields
    > > > SomeEnum['red']
    <SomeEnum.RED: 1>

    > > > SomeEnum('red')
    <SomeEnum.RED: 1>
    """

    # ===== methods for Pydantic validations =====
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, var: object):
        if isinstance(var, str):
            # noinspection PyArgumentList
            return cls(var)
        elif issubclass(var.__class__, cls):
            return var
        else:
            raise ValueError(f'Value must "str", not {var.__class__}')
