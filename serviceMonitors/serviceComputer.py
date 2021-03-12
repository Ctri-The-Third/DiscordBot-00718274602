import os
import subprocess
from models.service import * 
from wakeonlan import send_magic_packet

#all service requests should get a name, type in JSON, then specific config settings

class ServiceComputer(Service):
    serverMacAddress = ''
    serviceName = ''
    serviceType =''
    host = ''
    shutdownCommand = ''
    _statusEmoji = ":black_large_square:"
    _statusText = "Not checked yet"


    def __init__(self,serviceName, serviceType,  host, shutdownCommand, serverMacAddress ):
        super().__init__(serviceName,serviceType) 
        
        self.serviceType = serviceType
        self.serviceName = serviceName
        self.serverMacAddress = serverMacAddress        
        self.shutdownCommand = shutdownCommand
        self.host = host
            
    async def checkService(self):
        arg = "c" if os.name == 'posix' else "n"
        response=os.system("ping -%s 1 %s" % (arg,self.host))

        if response == 0:
            self._statusEmoji = ":green_square:"
            self._statusText = "online"
        else:
            self._statusEmoji = ":snowflake:"
            self._statusText = "offline"
        return

    def getFriendlyName(self):
        return self.serviceName
        
    def getStatusEmoji(self):
        return self._statusEmoji

    def getStatusText(self):
        return self._statusText

    async def tryStartService(self ):
        send_magic_packet('18-c0-d4-49-59-d0')
    
    def tryStopService(self):
        os.system(self.shutdownCommand)

if __name__ == '__main__':
    s = ServiceComputer(":desktop: Ramoth","server","serviceControls\\sleepRamoth.bat","18-c0-d4-49-59-d0")
    s.tryStartService()