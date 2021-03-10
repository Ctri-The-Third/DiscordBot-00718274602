import json



class Service():
    serviceName = ""
    serviceType = ""
    def __init__(self,serviceName,serviceType):
        self.serviceName = serviceName
        self.serviceType = serviceType
    
    def checkService(self):
        return

    def getFriendlyName(self):
        return self.serviceName

    def getStatusEmoji(self):
        return "⬛"

    def getStatusText(self):
        return "Unsupported service found!"
