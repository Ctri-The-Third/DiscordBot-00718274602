import requests
import os 
from models.service import * 

#all service requests should get a name, type in JSON, then specific config settings

class ServicePresence(Service):
     
    
    _statusEmoji = ":black_large_square:"
    _statusText = "Not checked yet"
    _enableds = 0
    _disableds = 0


    def __init__(self,serviceName, serviceType, prefixEmoji = None, presenceHost = None, presencePort = None, presenceKey = None ):
        super().__init__(serviceName,serviceType) 
        self.presenceHost = presenceHost
        self.presencePort = presencePort
        self.presenceKey = presenceKey
        self.prefixEmoji = prefixEmoji
        
    async def checkService(self):
        headers = self._getHeaders()
        url = self._getURL()
        try:
            response = requests.get(url=url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            self._statusText = "could not connect to host"
            self._statusEmoji = ":red_square:"
            return 
        if response.status_code != 200:
            self._statusText = "invalid status code"
            self._statusEmoji = ":red_square:"
        elif response.status_code == 200:
            self._enableds = 0
            self._disableds = 0
            
            statusObj = json.loads(response.content)
            self._recursiveCheck(statusObj)

            if self._enableds == 0:
                self._statusText = "Active, but services off"
                self._statusEmoji = ":red_square:"
            elif self._disableds == 0:
                self._statusText = "All services on"
                self._statusEmoji = ":green_square:"
            else:
                self._statusText = "{0} on, {1} off".format(self._enableds,self._disableds)
                self._statusEmoji = ":yellow_square:"


        return 
        
    def _recursiveCheck(self,dictOrString):
        if isinstance(dictOrString,dict):
            for key in dictOrString:
                self._recursiveCheck(dictOrString[key])
        elif isinstance(dictOrString,str):
            if dictOrString == "enabled":
                self._enableds += 1
            else:
                dictOrString == "disabled"
                self._disableds += 1

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

    def _getHeaders(self) -> dict:
        headers = {"Authorization": "Basic {0}".format(self.presenceKey)}
        return headers
    def _getURL(self) -> str:
        return "http://{0}:{1}/".format(self.presenceHost,self.presencePort)

    def cmdWorkTasksEnable(self,userID):
        if not self.checkAuthUser(userID):
            return 
        self._cmdWorkTasksToggle("true")

    def cmdWorkTasksDisable(self,userID):
        if not self.checkAuthUser(userID):
            return 
        self._cmdWorkTasksToggle("false")

    def _cmdWorkTasksToggle(self,newState):
        url = "{}{}{}".format(self._getURL(),"servicecontrol/worktasks/",newState)
        headers = self._getHeaders()
        result = requests.post(url=url,headers=headers)
        print(result)


    def cmdTriggerShutdown(self, userID):
        return 

    def cmdPurgeInbox(self,userID):
        if not self.checkAuthUser(userID):
            return
        self._cmdPurgeInbox()

    def _cmdPurgeInbox(self):
        services = [
            ["habitica", False],
            ["freshdesk",False],
            ["zendesk",False],
            ["jira",True],
            ["gmail",True]]
        
        for service in services:
            serviceName = service[0]
            subservice = service[1]
            url = "{url}{servicename}/purge/{subserviceaddition}{purgeLevel}".format(
                url=self._getURL(),
                servicename=serviceName,
                subserviceaddition = "*/" if subservice else "",
                purgeLevel = self._purgeLevel)
            headers = self._getHeaders()
            requests.post(url = url, headers = headers)
        
        



if __name__ == '__main__':
    settings = json.load(open("services.json"))
    s = ServicePresence("Presence","Presence","🟣","home.ctri.co.uk",9369,settings[4]["serviceKey"])