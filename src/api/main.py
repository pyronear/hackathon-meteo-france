import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import fwi

logger = logging.getLogger(__name__)

app = FastAPI(
    title="PYRORISK API",
    description="An API to manage the Pyrorisk application built during Meteo France Hackathon",
    docs_url="/",
    version="0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(fwi.router)


if __name__ == "__main__":
    # NOTE: this commands enables better development
    #  by reloading whenever some code is modified.
    uvicorn.run("main:app", host="0.0.0.0", port=80, workers=2, reload=True)
