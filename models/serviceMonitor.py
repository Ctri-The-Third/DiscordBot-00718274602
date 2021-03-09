
import json
from models.service import * 
from serviceMonitors.serviceValheim import *

_monitor = None


async def getActiveMonitor():
    global _monitor
    if _monitor is None:
        _monitor = monitor()
        await _monitor.doServiceUpdate()
    return _monitor


class monitor:
    _services = []
    def __init__(self):
        self.loadConfig()
        

    def getServiceListText(self):
        return ""

    def getServiceStatusText(self):
        return ""


    def loadConfig(self):
        self._services = [] 
        configFile = open("services.json","r")
        servicesList = json.load(configFile)
        for serviceJSON in servicesList:  
            if serviceJSON["serviceType"] == "valheim":
                valheimServer = ServiceValheim(serviceJSON["serviceName"],serviceJSON["serviceType"],"IP ADDRESS", "STATUS PORT")
                self._services.append(valheimServer)
            else: 
                genericService = Service(serviceJSON["serviceName"],serviceJSON["serviceType"])
                self._services.append(genericService)

    async def doServiceUpdate(self):
        print("Ready to update all services")

if __name__ == "__main__":
    monitor = getActiveMonitor()
    print(monitor)
    