from typing import Any, Literal

from sqlalchemy.orm import InstrumentedAttribute


def get_comparison(
    attr: InstrumentedAttribute,
    value: Any,
    is_not: bool = False,
    greater_then_comp: Literal["gt", "le"] | None = None,
):
    if value is None:
        return attr.is_(None) if not is_not else attr.isnot(None)
    else:
        if greater_then_comp is not None:
            if greater_then_comp == "gt":
                return attr.__gt__(value) if not is_not else attr.__le__(value)
            else:
                return attr.__le__(value) if not is_not else attr.__gt__(value)
        else:
            return attr.__eq__(value) if not is_not else attr.__ne__(value)
