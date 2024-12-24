import logging
from pathlib import Path
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles


FRONTEND_DIST = Path(__file__).resolve().parents[4] / "frontend" / "dist"

logging.info("FRONTEND_DIST: %s", FRONTEND_DIST)

router = APIRouter(tags=["webapp"])

router.mount(
    path="/app",
    app=StaticFiles(directory=str(FRONTEND_DIST), html=True),
    name="static"
    )
