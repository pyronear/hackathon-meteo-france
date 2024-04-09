import logging

from fastapi import APIRouter, Body

from src.api.schemas.wildfires import WildfiresLoadInput, WildfiresLoadOutput
from src.api.services.wildfires import load_wildfires_data

logger = logging.getLogger(__name__)

__all__ = ["router"]

router = APIRouter(
    prefix="/wildfires",
    tags=["wildfires"],
)


@router.post(
    "/load",
    status_code=202,
    response_model=WildfiresLoadOutput,
    summary="Load FWI from Copernicus.",
)
def load(
    load_input: WildfiresLoadInput,
) -> WildfiresLoadOutput:
    return WildfiresLoadOutput(**load_wildfires_data(load_input))
