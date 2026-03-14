def strip_to_none(string: str) -> str | None:
    if string is None:
        return None
    string = string.strip()
    return string if string else None
