from enum import Enum
from typing import Mapping

from pydantic import Field, BaseModel


class MonitoringMetricType(Enum):
    """ Available monitoring metric types """
    Gauge = "Gauge"
    Counter = "Counter"


class MonitoringMetric(BaseModel):
    """
        Central, universal schema for a monitoring metric.
        This metric will be converted by a (Prometheus) metrics converter for providing application monitoring metrics.
    """
    name: str = Field(description="Name of that metrics", example="")
    description: str = Field(description="Description of that metrics", example="")
    labels: Mapping[str, str] = Field(description="Custom labels for that metric",
                                      example={"label1": "value1", "label2": "value2"})
    type: MonitoringMetricType = Field(description="Type of monitoring metric (Gauge or Counter)",
                                       example=MonitoringMetricType.Gauge)
    value: float = Field(description="Numerical value of that metric", example=3.54)
