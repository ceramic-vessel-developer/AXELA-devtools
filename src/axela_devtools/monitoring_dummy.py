import sys
import os

sys.path.append(os.path.dirname(__file__))
from monitoring import MonitoringHandler

CLASS_NAME = "DummyMonitoringHandler"

class DummyMonitoringHandler(MonitoringHandler):
    def check_darkness_level(self):
        print("check_darkness_level wywołane")

    def check_camera_status(self):
        print("check_camera_status wywołane")

    def check_outdoor(self):
        print("check_outdoor wywołane")
