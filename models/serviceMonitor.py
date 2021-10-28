
import json
from models.service import *
from serviceMonitors.serviceValheim import *
from serviceMonitors.serviceComputer import * 
from serviceMonitors.servicePresence import * 

_staticMonitor = None


async def getActiveMonitor():
    global _staticMonitor
    if _staticMonitor is None:
        _staticMonitor = monitor()
        #await _staticMonitor.doServiceUpdate()
    return _staticMonitor


class monitor:
    _services = []
    def __init__(self):
        self.loadConfig()
    
    def getServices(self, serviceType = None):
        if serviceType == None:
            return self._services
        returnObj = []
        for service in self._services:
            if service.serviceType == serviceType:
                returnObj.append(service)
        return returnObj
        

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

    def getServiceByMenyEmoji(self, emoji):
        for service in self._services:
            if service.prefixEmoji is not None and service.prefixEmoji == emoji:
                return service
        return None

    def loadConfig(self):
        self._services = [] 
        configFile = open("services.json","r", encoding="utf-8")
        servicesList = json.load(configFile)
        for serviceJSON in servicesList:  
            prefixEmoji = None if "prefixEmoji" not in serviceJSON else serviceJSON["prefixEmoji"]
            shutdownCommand  = None if "shutdownCommand" not in serviceJSON else serviceJSON["shutdownCommand"]
            if serviceJSON["serviceType"] == "valheim":
                valheimServer = ServiceValheim(serviceJSON["serviceName"],serviceJSON["serviceType"],serviceJSON["host"],serviceJSON["statusPort"],serviceJSON["startupCommand"],shutdownCommand, prefixEmoji= prefixEmoji)
                self._services.append(valheimServer)
                if "guilds" in serviceJSON:
                    for guildName in serviceJSON["guilds"]:
                        valheimServer.registerGuild(guildName)
                else:
                    logging.warn("valheim server %s does not have a guilds array associated with it.")
            elif serviceJSON["serviceType"] == "server":
                MACAddress = None if "serverMacAddress" not in serviceJSON else serviceJSON["serverMacAddress"]
                computerService = ServiceComputer(serviceJSON["serviceName"],serviceJSON["serviceType"],serviceJSON["host"],shutdownCommand = shutdownCommand, serverMacAddress = MACAddress, prefixEmoji = prefixEmoji)
                self._services.append(computerService)
            elif serviceJSON["serviceType"] == "presence":
                serviceName = None if "serviceName" not in serviceJSON else serviceJSON["serviceName"]
                serviceType = None if "serviceType" not in serviceJSON else serviceJSON["serviceType"]
                prefixEmoji = None if "prefixEmoji" not in serviceJSON else serviceJSON["prefixEmoji"]
                hostname = None if "serviceHost" not in serviceJSON else serviceJSON["serviceHost"]
                port = None if "servicePort" not in serviceJSON else serviceJSON["servicePort"]
                authKey = None if "serviceKey" not in serviceJSON else serviceJSON["serviceKey"]
                presenceService = ServicePresence(serviceName,serviceType,prefixEmoji,hostname,port,authKey)
                self._services.append(presenceService) 
            else: 
                genericService = Service(serviceJSON["serviceName"],serviceJSON["serviceType"])
                self._services.append(genericService)

    async def doServiceUpdate(self):
        for service in self._services:
            await service.checkService()
        

if __name__ == "__main__":
    monitor = getActiveMonitor()
    print(monitor)
    