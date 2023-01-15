import json
import logging
import requests
from typing import List

from singleton_decorator import singleton

from core.monitoring_metrics.abstract_monitoring_metrics_provider import AMonitoringMetricsProvider
from core.monitoring_metrics.prometheus.model.monitoring_metric import MonitoringMetric, MonitoringMetricType
from core.monitoring_metrics.prometheus.monitoring_metrics_service import MonitoringMetricsManager

# get logger for that module
LOGGER = logging.getLogger(__name__)


@singleton
class RandomFactsService(AMonitoringMetricsProvider):

    def __init__(self):
        LOGGER.info("Starting Random Facts Service")

        MonitoringMetricsManager().register_as_provider(self)

        self._counter = 0

    def get_random_cat_facts(self):
        response = requests.get("https://catfact.ninja/fact")
        json_response = json.loads(response.text)
        self._counter += 1
        return json_response["fact"]

    def collect_monitoring_metrics(self):
        # return list for metrics
        metrics: List[MonitoringMetric] = [MonitoringMetric(
            name="random_facts_api_execution_counter",
            description="Counter of number of executions to get random facts about cats",
            labels={"service": "RandomFactsService"},
            type=MonitoringMetricType.Counter,
            value=self._counter
        )]

        return metrics
