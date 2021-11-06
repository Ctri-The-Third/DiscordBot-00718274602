import re
import discord
import datetime
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


    def __init__(self, presenceService, targetUser, message = None):
        if message is not None: 
            self.message = message
        else:
            self.messageText = _MESSAGE_CONTENT.format(presenceService.serviceName)
        self.presenceService = presenceService
        self.targetUser = targetUser


    async def _sendMessage(self):
        newMessage = await self.targetUser.send(content=self.messageText, embed = self.messageEmbed)
        self.message =  newMessage
        await self.message.add_reaction("🟢")
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
        serviceText = """🟢 to enable weekend mode
😴 to trigger darkness
📤 to purge inbox"""

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
        print("woooo")
        return 


def isPresenceMessage(discordMessage):
    result =  re.match(r"\*\*.* online, awaiting command\*\*",discordMessage.clean_content)
    return not (result == None)

def getPresenceMessageFromDiscordMessage(discordMessage):
    if isPresenceMessage(discordMessage):
        presenceMessage(discordMessage.channel,message=discordMessage)