import requests
import json
from models.service import *
 
#all service requests should get a name, type in JSON, then specific config settings

class ServiceValheim(Service):
    serverHost = ''
    serverStatusPort = ''
    serviceName = ''
    serviceType =''

    _statusEmoji = ":black_square:"
    _statusText = "Not checked yet"
    def __init__(self,serviceName, serviceType,serverHost, serverStatusPort):
        super().__init__(serviceName,serviceType) 
        self.serverHost = serverHost
        self.serverStatusPort = serverStatusPort
        self.serviceType = serviceType
        self.serviceName = serviceName

            
    def checkService(self):
        url = "http://%s:%s/status.json" % (self.serverHost,self.serverStatusPort)
        try:
            response = requests.get(url)
        except:
            self._statusEmoji = ":red_square:"
            self._statusText = "Server unreachable"
            return
        if response.status_code == 200:
            servercont = {}
            try:
                serverStatus = json.loads(response.content)
            except:
                self._statusEmoji = ":red_square:"
                self._statusText = "Invalid response"
            if "player_count" in serverStatus:
                self._statusEmoji = ":green_square:"
                self._statusText = "%s/10 players" % (serverStatus["player_count"])
            else: 
                self._statusEmoji = ":yellow_square:"
                self._statusText = "Probably waking up"

        # throw in the box active but server inactive
        return

    def getFriendlyName(self):
        return self.serviceName
        
    def getStatusEmoji(self):
        return self._statusEmoji

    def getStatusText(self):
        return self._statusText


