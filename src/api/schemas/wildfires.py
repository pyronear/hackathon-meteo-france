from typing import Any, Dict, List

from pydantic import BaseModel, Field


class WildfiresLoadInput(BaseModel):
    date: str = Field(..., description="The date of the data to load.")


class WildfiresLoadOutput(BaseModel):
    type: str
    features: List[Dict[str, Any]]
