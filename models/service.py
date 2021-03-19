import json



class Service():
    serviceName = ""
    serviceType = ""
    prefixEmoji = ""
    def __init__(self,serviceName,serviceType, prefixEmoji = None):
        self.serviceName = serviceName
        self.serviceType = serviceType
        self.prefixEmoji = prefixEmoji
    
    async def checkService(self):
        return

    def getFriendlyName(self):
        return self.serviceName

    def getStatusEmoji(self):
        return "⬛"

    def getStatusText(self):
        return "Unsupported service found!"

    def getMenuEmoji(self):
        return None
