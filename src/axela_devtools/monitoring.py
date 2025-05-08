from abc import ABC, abstractmethod

class MonitoringHandler(ABC):

    @abstractmethod
    def check_darkness_level(self):
        pass

    @abstractmethod
    def check_camera_status(self):
        pass

    @abstractmethod
    def check_outdoor(self):
        pass
