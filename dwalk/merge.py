from copy import deepcopy
from typing import Any, Dict, Optional


def merge(
    from_dict: Dict[Any, Any],
    from_src: Optional[str],
    to_dict: Dict[Any, Any],
) -> None:
    """
    Merges two dictionaries.

    Args:
        from_dict:     Source dictionary.

        from_filename: Optional path and filename of the `from_dict` dictionary.

                       If set, a `__KEY:dwalk:src__` key will be added as a
                       sibling of every key added or overwritten by this merge.

        to_dict:       Destination dictionary.
    """
    for key in from_dict:
        if key not in to_dict or not isinstance(from_dict[key], dict):
            to_dict[key] = deepcopy(from_dict[key])
            if from_src:
                to_dict[f"__{key}:dwalk:src__"] = from_src
        else:
            merge(
                from_dict=from_dict[key],
                from_src=from_src,
                to_dict=to_dict[key],
            )
