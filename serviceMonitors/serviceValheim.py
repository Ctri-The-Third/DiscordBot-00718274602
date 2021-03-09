import requests
from models.service import *
 
#all service requests should get a name, type in JSON, then specific config settings

class ServiceValheim(Service):
    serverHost = ''
    serverStatusPort = ''
    def __init__(self,serviceName, serviceType,serverHost, serverStatusPort):
        super().__init__(serviceName,serviceType) 
        self.serverHost = serverHost
        self.serverStatusPort = serverStatusPort

    