"""Prerequisite expression tree.

Three node types only:
  {"op": "and" | "or", "items": [<node>, ...]}
  {"course": "<uuid>"}
  {"min_credits": <int>}
"""

import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class CourseNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course: uuid.UUID


class MinCreditsNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_credits: int = Field(gt=0)


class GroupNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["and", "or"]
    items: list["PrereqNode"] = Field(min_length=1)


PrereqNode = Annotated[GroupNode | CourseNode | MinCreditsNode, Field(union_mode="left_to_right")]
GroupNode.model_rebuild()

_adapter: TypeAdapter[PrereqNode] = TypeAdapter(PrereqNode)


def validate_prereq_tree(value: object) -> dict:
    """Validate a raw tree and return its canonical JSON-able dict. Raises ValueError."""
    node = _adapter.validate_python(value)
    return _adapter.dump_python(node, mode="json")
