
import json
from models.service import * 
from serviceMonitors.serviceValheim import *
from serviceMonitors.serviceComputer import * 
_staticMonitor = None


async def getActiveMonitor():
    global _staticMonitor
    if _staticMonitor is None:
        _staticMonitor = monitor()
        await _staticMonitor.doServiceUpdate()
    return _staticMonitor


class monitor:
    _services = []
    def __init__(self):
        self.loadConfig()
        
    def getServices(self):
        return self._services

    async def getServiceListText(self):
        returnString = ""
        for service in self._services:
            if service.serviceType != "server":
                returnString = returnString + "> %s\n" % (service.getFriendlyName())
        return returnString

    async def getServiceStatusText(self):
        returnString = ""
        for service in self._services:
            if service.serviceType != "server":
                returnString = returnString + "%s `%s`\n" % (service.getStatusEmoji(), service.getStatusText())
        return returnString

    async def getServerListText(self):
        returnString = ""
        for service in self._services:
            if service.serviceType == "server":
                returnString = returnString + "> %s\n" % (service.getFriendlyName())
        return returnString

    async def getServerStatusText(self):
        returnString = ""
        for service in self._services:
            if service.serviceType == "server":
                returnString = returnString + "%s `%s`\n" % (service.getStatusEmoji(), service.getStatusText())
        return returnString

    def loadConfig(self):
        self._services = [] 
        configFile = open("services.json","r")
        servicesList = json.load(configFile)
        for serviceJSON in servicesList:  
            if serviceJSON["serviceType"] == "valheim":
                valheimServer = ServiceValheim(serviceJSON["serviceName"],serviceJSON["serviceType"],serviceJSON["host"],serviceJSON["statusPort"],serviceJSON["startupCommand"],serviceJSON["shutdownCommand"])
                self._services.append(valheimServer)
            elif serviceJSON["serviceType"] == "server":
                computerService = ServiceComputer(serviceJSON["serviceName"],serviceJSON["serviceType"],serviceJSON["host"],serviceJSON["shutdownCommand"],serviceJSON["serverMacAddress"])
                self._services.append(computerService)
            else: 
                genericService = Service(serviceJSON["serviceName"],serviceJSON["serviceType"])
                self._services.append(genericService)

    async def doServiceUpdate(self):
        for service in self._services:
            await service.checkService()
        

if __name__ == "__main__":
    monitor = getActiveMonitor()
    print(monitor)
    