import math
from typing import Optional, Tuple

OPS = {
    ">=": ">=",
    "<=": "<=",
    ">": ">",
    "<": "<",
    "==": "=",
    "=": "=",
}

def parse_number_or_none(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        if isinstance(val, float) and math.isnan(val):
            return None
        return val
    s = str(val).strip()
    if s.lower() == "nan" or s == "":
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None

def parse_op_value(s: Optional[str]) -> Tuple[str, Optional[float]]:
    if not s:
        return "=", None
    s = s.strip()
    for op in [">=", "<=", ">", "<", "==", "="]:
        if s.startswith(op):
            num = s[len(op):].strip()
            try:
                return OPS[op], float(num)
            except ValueError:
                return OPS[op], None
    # default equals
    try:
        return "=", float(s)
    except ValueError:
        return "=", None
