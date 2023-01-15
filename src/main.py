import logging

import uvicorn
import core.logging as core_logging

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware

from api import get_prometheus_metrics, get_random_cat_facts
from modules.random_facts_service import RandomFactsService

# setup root logger
core_logging.setup_root_logger()

# Get logger for module
LOGGER = logging.getLogger(__name__)

LOGGER.info("---Starting App---")

app = FastAPI()

# Add middleware for prometheus monitoring (mainly for request time buckets monitoring)
app.add_middleware(PrometheusMiddleware)


@app.on_event("startup")
def exec_on_startup():
    RandomFactsService()


# Monitoring metrics
app.include_router(get_prometheus_metrics.router)
# Random Facts
app.include_router(get_random_cat_facts.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
