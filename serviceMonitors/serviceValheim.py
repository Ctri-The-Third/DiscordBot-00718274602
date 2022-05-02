from http import server
import os
import requests
import json
import datetime
from models.service import *
import logging
import threading 
#all service requests should get a name, type in JSON, then specific config settings

class ServiceValheim(Service):
    serverHost = ''
    serverStatusPort = ''
    serviceName = ''
    serviceType =''
    startupCommand = ''
    shutdownCommand = ''
    lastOccupied = None
    prefixEmoji = ""
    _statusEmoji = ":black_large_square:"
    _statusText = "Not checked yet"


    def __init__(self,serviceName, serviceType,serverHost, serverStatusPort, startupCommand, shutdownCommand, prefixEmoji = None):
        super().__init__(serviceName,serviceType) 
        self.serverHost = serverHost
        self.serverStatusPort = serverStatusPort
        self.serviceType = serviceType
        self.serviceName = serviceName
        self.startupCommand = startupCommand
        self.shutdownCommand = shutdownCommand
        self.lastOccupied = datetime.datetime.now()
        self.validGuilds = []
        if prefixEmoji is not None:
            self.prefixEmoji = prefixEmoji
            
    def registerGuild(self, guild):
        if guild not in self.validGuilds:
            self.validGuilds.append(guild)

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
            self.lastOccupied = None
            #print(e)
            return
        
        if response.status_code == 200:
            servercont = {}
            try:
                serverStatus = json.loads(response.content)
                if "player_count" in serverStatus:
                    self._statusEmoji = ":green_square:"
                    self._statusText = "%s/10 players" % (serverStatus["player_count"])
                    playerCount = serverStatus["player_count"]
                else: 
                    self._statusEmoji = ":yellow_square:"
                    self._statusText = "Probably waking up"
                    self.lastOccupied = datetime.datetime.now()    
            except:
                self._statusEmoji = ":red_square:"
                self._statusText = "Invalid response"

        if playerCount > 0 or self.lastOccupied is None:
            self.lastOccupied = datetime.datetime.now()
        else: 

            timeSinceOccupied = datetime.datetime.now() - self.lastOccupied 
            logging.info("Server [%s]- time since last occupied: %s" % (self.getFriendlyName(),timeSinceOccupied))
            if timeSinceOccupied.seconds > 1200:
                await self.tryStopService()
        # throw in the box active but server inactive
        return

    def getFriendlyName(self):
        if self.prefixEmoji is not None:
            return "%s %s" % (self.prefixEmoji,self.serviceName)
        else:
            return self.prefixEmoji
        
    def getStatusEmoji(self):
        return self._statusEmoji

    def getMenuEmoji(self):
        if self.shutdownCommand is None and self.startupCommand is None:
            return None
        else:
            return self.prefixEmoji

    def getStatusText(self):
        return self._statusText

    async def tryStartService(self, guild = None, server_name= "*" ):
        if guild is None or guild.name in self.validGuilds:   
            if server_name.lower() == self.serviceName.lower() or server_name == "*":
                t = threading.Thread(target=self._startService )
                t.start()
                self.lastOccupied = datetime.datetime.now() 
                return True
        return False
    async def tryStopService(self):
        os.system(self.shutdownCommand)

        return 
    def _startService (self):
        logging.info("Starting valheim service %s" % (self.getFriendlyName()))
        os.system(self.startupCommand)
        logging.info("Completed attempt to start valheim service %s" % (self.getFriendlyName()))