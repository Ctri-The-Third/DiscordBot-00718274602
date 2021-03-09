import discord
import datetime



class statusMessage:
    messageEmbed = None
    message = None
    messageState = None
    messageText = None
    messageFooter = None
    channel = None
    services = {}

    async def _sendMessage(self):
        self.message = await self.channel.send(content=self.messageText, embed = self.messageEmbed)
        pass

    async def sendOrUpdate(self):
        await self._updateEmbed()
        if self.message is not None:
            #update
            pass
        else:
            self.message = await self._sendMessage()
            #send 
    


    async def _editMessage(self):
        return 

    async def _updateEmbed(self):
        if self.messageEmbed is None:
            self._createEmbed()
        self.messageEmbed.set_footer(text=self._getFooter())
        return 

    def _createEmbed(self):
        messageEmbed = discord.Embed()
        
        messageEmbed.add_field(name = "Service", value = self._getEmbedServicesList(), inline=True)
        messageEmbed.add_field(name = "Status", value = self._getEmbedStatusList(), inline=True)
        messageEmbed.colour = discord.Colour.green()

        self.messageEmbed = messageEmbed

    def _getEmbedServicesList(self):
        servicesTxt = ""
        for service in self.services:
            servicesTxt = servicesTxt + "> %s\n" % (service)
        return servicesTxt

    def _getEmbedStatusList(self):
        statusText = ""
        for service in self.services:
            statusText = statusText + "%s `%s`\n" % (self.services[service]['symbol'],self.services[service]['text'])
        return statusText


    def _getFooter(self):
        return "Last updated %s" % datetime.datetime.now().strftime(r'%Y-%b-%d %H:%M:%S')


    def checkServices(self):
        services = self.services
        services["bot"] = {"symbol":"🟩","text":"active"}
        services["Vserver - Hordelings"] = {"symbol":"🟩","text":"online [?/10]"}
        services["Vserver - deltaPals"] = {"symbol":"🟨","text":"offline warm"}
        services["Presence"] = {"symbol":"🟩","text":"active"}
        services["LaserScraper"] = {"symbol":"🟩","text":"idle"}

        return

    def __init__(self, channel ,message = None):
        if message is not None: 
            self.message = message
        else:
            self.messageText = """**Information requested:** Service status
Beginning report..."""
        self.channel = channel #discord.channel

    