import logging

from fastapi import APIRouter, status
from starlette.responses import PlainTextResponse

from modules.random_facts_service import RandomFactsService

# get logger for that module
logger = logging.getLogger(__name__)

# initialize router for FastAPI (REST API)
router = APIRouter()


@router.get('/cat_facts',
            response_class=PlainTextResponse,
            status_code=status.HTTP_200_OK,
            tags=["Random Facts - read"])
def get_random_cat_facts():
    """ Provides random facts about cats """

    return RandomFactsService().get_random_cat_facts()
