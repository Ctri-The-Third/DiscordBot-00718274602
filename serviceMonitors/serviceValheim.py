import os
import requests
import json
import datetime
from models.service import *
 
#all service requests should get a name, type in JSON, then specific config settings

class ServiceValheim(Service):
    serverHost = ''
    serverStatusPort = ''
    serviceName = ''
    serviceType =''
    startupCommand = ''
    shutdownCommand = ''
    lastOccupied = None
    _statusEmoji = ":black_large_square:"
    _statusText = "Not checked yet"


    def __init__(self,serviceName, serviceType,serverHost, serverStatusPort, startupCommand, shutdownCommand):
        super().__init__(serviceName,serviceType) 
        self.serverHost = serverHost
        self.serverStatusPort = serverStatusPort
        self.serviceType = serviceType
        self.serviceName = serviceName
        self.startupCommand = startupCommand
        self.shutdownCommand = shutdownCommand
        self.lastOccupied = datetime.datetime.now()
            
    async def checkService(self):
        url = "http://%s:%s/status.json" % (self.serverHost,self.serverStatusPort)
        playerCount = 0 
        try:
            response = requests.get(url,timeout=5)
            
            if response == None:
                raise Exception("Did not receive response from server")
            
        except Exception as e:
            self._statusEmoji = ":red_square:"
            self._statusText = "Server unreachable"
            print(e)
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
                playerCount = serverStatus["player_count"]
            else: 
                self._statusEmoji = ":yellow_square:"
                self._statusText = "Probably waking up"
        if playerCount > 0:
            self.lastOccupied = datetime.datetime.now()
        else: 
            timeSinceOccupied = datetime.datetime.now() - self.lastOccupied 
            print("Server [%s]- time since last occupied: %s" % (self.getFriendlyName(),timeSinceOccupied))
            if timeSinceOccupied.seconds > 1200:
                self.tryStopService()
        # throw in the box active but server inactive
        return

    def getFriendlyName(self):
        return self.serviceName
        
    def getStatusEmoji(self):
        return self._statusEmoji

    def getStatusText(self):
        return self._statusText

    async def tryStartService(self ):
    
        os.system(self.startupCommand)
        self.lastOccupied = datetime.datetime.now()
        return 
    def tryStopService(self):
        os.system(self.shutdownCommand)

        return 
