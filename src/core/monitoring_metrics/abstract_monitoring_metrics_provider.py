from abc import abstractmethod, ABCMeta


class AMonitoringMetricsProvider(metaclass=ABCMeta):
    """ This interface has to be implemented by modules which want to register as monitoring metrics provider """

    @abstractmethod
    def collect_monitoring_metrics(self):
        """ Deliver all monitoring metrics from a specific module """
        raise NotImplementedError
