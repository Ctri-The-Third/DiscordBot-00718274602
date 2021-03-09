import json



class Service():
    serviceName = ""
    serviceType = ""
    def __init__(self,serviceName,serviceType):
        self.serviceName = serviceName
        self.serviceType = serviceType
    
    def checkService(self):
        returnObject = {"statusEmoji":"⬛","statusText":"Generic service found!"}



