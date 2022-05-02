import re
import discord
import datetime
from models.service import Service
import models.serviceMonitor
import logging

_MESSAGE_CONTENT = "**{} online, awaiting command**"

class presenceMessage:

    messageEmbed = None
    message = None
    messageID = None
    messageText = None
    messageFooter = None
    serverListText = "None"
    serverStatusText = "⬛ no services checked"
    servicesListText = "None"
    servicesStatusText = "⬛ no services checked"
    channel = None
    presenceService = None
    destroyed = False


    def __init__(self, presenceService, targetUser = None, message = None):
        if message is not None: 
            self.message = message
        else:
            self.messageText = _MESSAGE_CONTENT.format(presenceService.serviceName)
        self.presenceService = presenceService
        self.targetUser = targetUser


    async def _sendMessage(self):
        if self.targetUser == None:
            #can't send a new message unless we know who triggered the !007 presence command.
            
            return 
        newMessage = await self.targetUser.send(content=self.messageText, embed = self.messageEmbed)
        self.message =  newMessage
        
        await self.message.add_reaction("🟢")
        await self.message.add_reaction("🔴")
        await self.message.add_reaction("😴")
        await self.message.add_reaction("📤")
    
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
        
        await reaction.message.remove_reaction(reaction.emoji,user)
        return

    async def _editMessage(self):
        return 


    async def _refreshEmbed(self):
        messageEmbed = discord.Embed()
        weekendMode = self.presenceService.checkWeekendMode()
        weekendText = ""
        serviceText = """🟢 to disable weekend mode
🔴 to enable weekend mode
😴 to trigger darkness
📤 to purge inbox""".format(weekendText)

        messageEmbed.add_field(name = "Commands", value = serviceText)
        

        messageEmbed.colour = discord.Colour.green()
        messageEmbed.set_footer(text=self._getFooter())

        self.messageEmbed = messageEmbed
    

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

    def on_reaction_add_raw(self,user,emoji_name):
        if user.bot:
            print("TODO - this method needs to NOT receive reaction adds from the bot itself.")
            return 
        if emoji_name  == "🟢" or emoji_name == "\U0001f7e2":
            self.presenceService.cmdWorkTasksEnable(user.id)
        elif emoji_name == "🔴":
            self.presenceService.cmdWorkTasksDisable(user.id)
        elif emoji_name == "😴":
            self.presenceService.cmdTriggerShutdown(user.id)
        elif emoji_name == "📤":
            self.presenceService.cmdPurgeInbox(user.id)
             
        return 


def isPresenceMessage(discordMessage):
    result =  re.match(r"\*\*(.*) online, awaiting command\*\*",discordMessage.clean_content)
    return not (result == None)

def getPresenceServiceName(discordMessage):
    result =  re.match(r"\*\*(.*) online, awaiting command\*\*",discordMessage.clean_content)
    return not (result == None)



async def getPresenceMessageFromDiscordMessage(discordMessage, user=None):
    if isPresenceMessage(discordMessage):
        #self, presenceService, targetUser = None, message = None
        monitor = await models.serviceMonitor.getActiveMonitor()
        services = monitor.getServices("presence")
        if len(services) > 1:
            logging.warn("There are multiple presence services, this is not supported")
        if len(services) >= 1:
            return presenceMessage( services[0],message=discordMessage,targetUser=user)
        else:
            logging.warn("There is no presence service configured")
