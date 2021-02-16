from typing import Any


# Get deeply nested values from JSON, only string keys allowed
# @param obj - dictionary to search for path
# @param path - dot separated path string
def get_by_path(obj: dict, path: str, default=None) -> Any:
    if not obj or not path:
        return obj

    keys = path.split('.')
    curr = obj

    for key in keys:
        if key not in curr:
            return default

        curr = curr[key]

    return curr
