import logging

from fastapi import APIRouter, Body

from src.api.schemas.fwi import FWILoadInput, FWILoadOutput
from src.api.services.fwi import load_fwi_data

logger = logging.getLogger(__name__)

__all__ = ["router"]

router = APIRouter(
    prefix="/fwi",
    tags=["fwi"],
)


@router.post(
    "/load",
    status_code=202,
    response_model=FWILoadOutput,
    summary="Load FWI from Copernicus.",
)
def load(
    load_input: FWILoadInput,
) -> FWILoadOutput:
    return FWILoadOutput(**load_fwi_data(load_input))
