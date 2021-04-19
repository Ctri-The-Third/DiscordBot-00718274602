
import os 
from models.service import * 

#all service requests should get a name, type in JSON, then specific config settings

class ServiceComputer(Service):
     
    serviceName = ''
    serviceType =''
    
    startupCommand = ''
    _statusEmoji = ":black_large_square:"
    _statusText = "Not checked yet"
    prefixEmoji = ""


    def __init__(self,serviceName, serviceType, prefixEmoji = None, startupCommand = None ):
        super().__init__(serviceName,serviceType) 
        
        self.serviceType = serviceType
        self.serviceName = serviceName
        self.prefixEmoji = prefixEmoji
        self.startupCommand = startupCommand        
    async def checkService(self):
        return 
        

    def getMenuEmoji(self):
        return 
        ### If no details/ interactables, return None

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
        os.system(self.startupCommand)

    def tryStopService(self):
        return 

if __name__ == '__main__':
    s = ServiceComputer(":desktop: Ramoth","server","serviceControls\\sleepRamoth.bat","18-c0-d4-49-59-d0")
    s.tryStartService()