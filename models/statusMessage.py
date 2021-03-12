import discord
import datetime
import models.serviceMonitor


class statusMessage:
    messageEmbed = None
    message = None
    messageState = None
    messageText = None
    messageFooter = None
    servicesListText = "None"
    servicesStatusText = "⬛ no services checked"
    channel = None
    
    destroyed = False

    async def _sendMessage(self):
        newMessage = await self.channel.send(content=self.messageText, embed = self.messageEmbed)
        self.message =  newMessage
        

    async def sendOrUpdate(self):
        await self._refreshEmbed()
        
        if self.message is not None:
            try:
                await self.message.edit(embed=self.messageEmbed)
            except Exception as e:
                print("Couldn't updpate status message \n %s" % e)
                destroyed = True
            return
        else:
            await self._sendMessage()
            return 
            #send 
    
    

    async def _editMessage(self):
        return 


    async def _refreshEmbed(self):

        serviceMonitorInstance = await models.serviceMonitor.getActiveMonitor()
        self.servicesListText = await serviceMonitorInstance.getServiceListText()
        self.servicesStatusText = await serviceMonitorInstance.getServiceStatusText()


        messageEmbed = discord.Embed()

        messageEmbed.add_field(name = "Service", value = self.servicesListText, inline=True)
        messageEmbed.add_field(name = "Status", value = self.servicesStatusText, inline=True)
        messageEmbed.colour = discord.Colour.green()
        messageEmbed.set_footer(text=self._getFooter())

        self.messageEmbed = messageEmbed
        return

    def setEmbedServicesList(self,string):
        self.servicesListText = string

    def setEmbedStatusList(self,string):
        self.servicesStatusText = string


    def _getFooter(self):
        return "Last updated %s" % datetime.datetime.now().strftime(r'%Y-%b-%d %H:%M:%S')



    def __init__(self, channel ,message = None):
        if message is not None: 
            self.message = message
        else:
            self.messageText = """**Information requested:** Service status
Beginning report..."""
        
        self.channel = channel #discord.channel

    