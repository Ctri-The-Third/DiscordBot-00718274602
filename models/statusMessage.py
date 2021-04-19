import discord
import datetime
import models.serviceMonitor
import logging

class statusMessage:
    messageEmbed = None
    message = None
    
    messageText = None
    messageFooter = None
    serverListText = "None"
    serverStatusText = "⬛ no services checked"
    servicesListText = "None"
    servicesStatusText = "⬛ no services checked"
    channel = None
    
    screenState = "rootMenu" #serviceDetail
    screenStateService = None
    destroyed = False

    async def _sendMessage(self):
        newMessage = await self.channel.send(content=self.messageText, embed = self.messageEmbed)
        self.message =  newMessage
        await self._setEmoji()
    
    async def _setEmoji(self):
        return #disabled for now
        if self.screenState == "rootMenu":
            activeMonitor = await models.serviceMonitor.getActiveMonitor()
            for service in activeMonitor.getServices():
                menuEmoji = service.getMenuEmoji()
                if menuEmoji is not None:
                    try:
                        
                        await self.message.add_reaction(menuEmoji)
                    except Exception as e:
                        logging.warn("unable to add menu reaction \n%s" % (e))
        else:
            await self.message.add_reaction("🚫")
        if self.screenState == "detail":
            return 

    

            

    async def sendOrUpdate(self):
        await self._refreshEmbed()
        
        if self.message is not None:
            try:
                logging.debug("EDITING MESSAGE %s" % (str(self.message.id)[0:10]))
                await self.message.edit(embed=self.messageEmbed)
            except Exception as e:
                logging.warn("Couldn't updpate status message \n %s" % e)
                self.destroyed = True
            return
        else:
            await self._sendMessage()
            return 
            #send 
    

    async def on_reaction_add(self,reaction,user):
        
        serviceMonitor = await models.serviceMonitor.getActiveMonitor()
        service = serviceMonitor.getServiceByMenyEmoji(reaction.emoji)
        if reaction.emoji == "🚫":
            self.screenState = "rootMenu"
            self.screenStateService = None
            

            await self._refreshEmbed()
            await self.sendOrUpdate()
            await reaction.message.clear_reactions()
            await self._setEmoji()
        if service is not None:
            self.screenState = "detail"
            self.screenStateService = service
            
            await self._refreshEmbed()
            await self.sendOrUpdate()
            await reaction.message.clear_reactions()
            await self._setEmoji()
            return
        #user has tried to enter a menu. 
        #based on the menu, set status message and refresh embed
        #clear reactions
        #set new reactions.
        await reaction.message.remove_reaction(reaction.emoji,user)
        return

    async def _editMessage(self):
        return 


    async def _refreshEmbed(self):
        if self.screenState == "detail":
            await self._refreshEmbedDetail()
        else:
            serviceMonitorInstance = await models.serviceMonitor.getActiveMonitor()
            self.servicesListText = await serviceMonitorInstance.getServiceListText()
            self.servicesStatusText = await serviceMonitorInstance.getServiceStatusText()
            self.serverListText = await serviceMonitorInstance.getServerListText()
            self.serverStatusText = await serviceMonitorInstance.getServerStatusText()

            messageEmbed = discord.Embed()

            if self.serverListText != '' and self.serverStatusText != '':
                messageEmbed.add_field(name="Server", value = self.serverListText, inline=True)
                messageEmbed.add_field(name = "Status", value = self.serverStatusText, inline=True)
                messageEmbed.add_field(name = "\u200b", value="\u200b", inline=True)
            messageEmbed.add_field(name = "Service", value = self.servicesListText, inline=True)
            messageEmbed.add_field(name = "Status", value = self.servicesStatusText, inline=True)

            messageEmbed.colour = discord.Colour.green()
            messageEmbed.set_footer(text=self._getFooter())

            self.messageEmbed = messageEmbed
        return

    async def _refreshEmbedDetail(self):
        messageEmbed = discord.Embed()
        self.messageEmbed = messageEmbed
        return 

    def setEmbedServicesList(self,string):
        self.servicesListText = string

    def setEmbedStatusList(self,string):
        self.servicesStatusText = string

    

    def _getFooter(self):
        return "\nLast updated %s" % datetime.datetime.now().strftime(r'%Y-%b-%d %H:%M:%S')
        return "Use the appropriate emojis to see more details on a given service.\nLast updated %s" % datetime.datetime.now().strftime(r'%Y-%b-%d %H:%M:%S')



    def __init__(self, channel ,message = None):
        if message is not None: 
            self.message = message
        else:
            self.messageText = """**Information requested:** Service status
Beginning report..."""
        
        self.channel = channel #discord.channel


def isStatusMessage(discordMessage):
    if discordMessage.content == """**Information requested:** Service status
Beginning report...""":

        return True
    return False

def getStatusMessageFromDiscordMessage(discordMessage, listOfStatusMessages):
    for statusMessage in listOfStatusMessages:
        try:
            if statusMessage.message.id == discordMessage.id:
                return statusMessage
        except:
            continue
    return None