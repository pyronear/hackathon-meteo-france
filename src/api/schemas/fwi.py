from typing import Any, Dict, List

from pydantic import BaseModel, Field


class FWILoadInput(BaseModel):
    date: str = Field(..., description="The date of the data to load.")


class FWILoadOutput(BaseModel):
    type: str
    crs: Dict[str, Any]
    features: List[Dict[str, Any]]
