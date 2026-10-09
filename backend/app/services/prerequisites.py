"""Conversion between flat prerequisite id lists and the prerequisite tree."""

import uuid
from typing import Any


class UnsupportedPrereqTree(ValueError):
    """The tree uses nodes that a plain AND list of courses cannot represent."""


def and_tree(course_ids: list[uuid.UUID]) -> dict[str, Any] | None:
    """[] -> None; [a] -> {"course": a}; [a, b, ...] -> {"op": "and", "items": [...]}.

    This is exactly what the frontend enforces today: every listed course must be approved.
    """
    if not course_ids:
        return None
    nodes = [{"course": str(c)} for c in course_ids]
    if len(nodes) == 1:
        return nodes[0]
    return {"op": "and", "items": nodes}


def flatten_and_tree(tree: dict[str, Any] | None) -> list[uuid.UUID]:
    """Inverse of and_tree. Raises UnsupportedPrereqTree for OR or min_credits nodes."""
    if tree is None:
        return []
    if "course" in tree:
        return [uuid.UUID(str(tree["course"]))]
    if tree.get("op") == "and":
        result: list[uuid.UUID] = []
        for item in tree["items"]:
            result.extend(flatten_and_tree(item))
        return result
    raise UnsupportedPrereqTree("prerequisite tree is not a plain AND of courses")
