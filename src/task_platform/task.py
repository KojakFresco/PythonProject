import attrs
from attrs import field, validators
from typing import Any


@attrs.define
class Task:
    id: str = field(validator=[validators.instance_of(str), validators.min_len(1)])
    payload: dict[str, Any] = field(
        factory=dict,
        validator=validators.instance_of(dict),
    )
