import os
import subprocess
from models.service import * 
from wakeonlan import send_magic_packet
import socket

#all service requests should get a name, type in JSON, then specific config settings

class ServiceComputer(Service):
    serverMacAddress = ''
    serviceName = ''
    serviceType =''
    host = ''
    shutdownCommand = ''
    _statusEmoji = ":black_large_square:"
    _statusText = "Not checked yet"
    prefixEmoji = ""


    def __init__(self,serviceName, serviceType,  host, shutdownCommand = None, serverMacAddress = None, prefixEmoji = None ):
        super().__init__(serviceName,serviceType) 
        
        self.serviceType = serviceType
        self.serviceName = serviceName
        self.serverMacAddress = serverMacAddress        
        self.shutdownCommand = shutdownCommand
        self.host = host
        self.prefixEmoji = prefixEmoji        
    async def checkService(self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try: 
            s.connect((self.host,22))
            self._statusEmoji = ":green_square:"
            self._statusText = "online"
        except socket.error as e:
            print("INFO: couldn't connect to %s, reason %s" % (self.serviceName,e))
            self._statusEmoji = ":zzz:"
            self._statusText = "offline"
        

    def getMenuEmoji(self):
        ### If no details/ interactables, return None
        if self.serverMacAddress is None:
            return None
        else:
            return self.prefixEmoji

    def getFriendlyName(self):
        if self.prefixEmoji is not None:
            return "%s %s" % (self.prefixEmoji,self.serviceName)
        else:
            return self.prefixEmoji
        
    def getStatusEmoji(self):
        return self._statusEmoji

    def getStatusText(self):
        return self._statusText

    async def tryStartService(self):
        if self.serverMacAddress is not None: 
            send_magic_packet(self.serverMacAddress)
    
    def tryStopService(self):
        os.system(self.shutdownCommand)

if __name__ == '__main__':
    s = ServiceComputer(":desktop: Ramoth","server","serviceControls\\sleepRamoth.bat","18-c0-d4-49-59-d0")
    s.tryStartService()