from typing import List, Dict, Any

import prometheus_client
from prometheus_client import Counter, Gauge
from singleton_decorator import singleton

from core.monitoring_metrics.abstract_monitoring_metrics_provider import AMonitoringMetricsProvider
from core.monitoring_metrics.prometheus.model.monitoring_metric import MonitoringMetric, \
    MonitoringMetricType


@singleton
class MonitoringMetricsManager:
    """ Collects and prepares monitoring metrics for specific monitoring systems (at the moment Prometheus only) """

    # save all instances of monitoring metrics providers
    monitoring_metrics_providers: List[AMonitoringMetricsProvider] = []

    # dict with all current metrics
    current_monitoring_metrics: Dict[str, Any] = {}

    # -------------------------------------------------------------------------
    # --- methods for providers -----------------------------------------------
    # -------------------------------------------------------------------------

    def register_as_provider(self, provider_instance: AMonitoringMetricsProvider):
        """ Registers a module as monitoring metrics provider.
        The Class has to implement AMonitoringMetricsProvider for that! """
        self.monitoring_metrics_providers.append(provider_instance)

    # -------------------------------------------------------------------------
    # --- methods for api -----------------------------------------------------
    # -------------------------------------------------------------------------

    def get_current_prometheus_monitoring_metrics(self):
        """ Main method for graping the current metrics (usually called by an API method) """

        # collect all metrics
        self._collect_monitoring_metrics_from_providers()

        return prometheus_client.generate_latest()

    def get_media_response_type(self):
        """ Provides the right media type for presenting (usually called by an API method) """
        return prometheus_client.CONTENT_TYPE_LATEST

    # -------------------------------------------------------------------------
    # --- internal helper methods ---------------------------------------------
    # -------------------------------------------------------------------------

    def _collect_monitoring_metrics_from_providers(self):
        """" Collects all monitoring metric from providers  """
        for provider in self.monitoring_metrics_providers:

            # collect metrics
            module_metrics = provider.collect_monitoring_metrics()

            # convert and save as prometheus metrics
            for module_metric in module_metrics:
                self._convert_and_save_as_prometheus_metric(module_metric)

    def _convert_and_save_as_prometheus_metric(self, metric: MonitoringMetric):
        """
            Converts a general monitoring metric to a prometheus monitoring metric.
            This method also saves that metric to the central prometheus system of the app (via prometheus_client).
        """

        # --- handle gauge monitoring metrics ---
        if metric.type == MonitoringMetricType.Gauge:

            if metric.name not in self.current_monitoring_metrics:
                self.current_monitoring_metrics[metric.name] = Gauge(metric.name, metric.description,
                                                                     metric.labels.keys())

            self.current_monitoring_metrics[metric.name].labels(**metric.labels).set(metric.value)

        # --- handle counter monitoring metrics ---
        elif metric.type == MonitoringMetricType.Counter:

            if metric.name not in self.current_monitoring_metrics:
                self.current_monitoring_metrics[metric.name] = Counter(metric.name, metric.description,
                                                                       metric.labels.keys())

            self.current_monitoring_metrics[metric.name].labels(**metric.labels).inc(metric.value)
