import logging

from fastapi import APIRouter, status, Response
from starlette.responses import PlainTextResponse

from core.monitoring_metrics.prometheus.monitoring_metrics_service import MonitoringMetricsManager

# get logger for that module
logger = logging.getLogger(__name__)

# initialize router for FastAPI (REST API)
router = APIRouter()


@router.get('/metrics',
            response_class=PlainTextResponse,
            status_code=status.HTTP_200_OK,
            tags=["Monitoring metrics - read"],
            response_description="Provides prometheus metrics")
def get_prometheus_metrics():
    """ Provides the current monitoring app metrics in prometheus format """

    # Get instance of the manager
    metrics_manager = MonitoringMetricsManager()

    # Return metrics
    return Response(metrics_manager.get_current_prometheus_monitoring_metrics(),
                    media_type=metrics_manager.get_media_response_type())
