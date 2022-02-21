import datetime

__all__ = [
    "datetime_validator",
]


def datetime_validator(var, now_if_none: bool = True):
    if isinstance(var, datetime.datetime):
        return var
    else:
        if isinstance(var, str):
            return datetime.datetime.fromisoformat(var.replace("Z", ""))
        else:
            if now_if_none is True:
                return datetime.datetime.utcnow()
            else:
                raise ValueError(f"Incompatible type: must be 'str' or 'datetime', found {type(var)}")
