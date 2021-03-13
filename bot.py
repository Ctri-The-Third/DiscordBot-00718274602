#pip install -U git+https://github.com/Rapptz/discord.py
import discord
import random
import json
import asyncio
import re
import handlers
import models.serviceMonitor as serviceMonitor
import models.statusMessage
import threading 


class Warforged(discord.Client):
    
    _statusMessages = []
    serviceMonitorInstance = None
    statusUpdaterLoop = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #detached loop not connected to the discord client for checking service



    def serviceUpdaterLoop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.serviceUpdater())
        loop.close()
    
    async def serviceUpdater(self):
        while not self.is_closed():
            #await channel.send("%s" % counter)
            
            await asyncio.sleep(5) # task runs every 60 seconds
            await self.serviceMonitorInstance.doServiceUpdate()
            print("thread2-heartbeat")


    async def updateStatusMessagesLoop(self):
        #service check should go here
        #status messages should be updated with text
        while True:
            for statusM in self._statusMessages:
                if statusM.destroyed:
                    self._statusMessages.remove(statusM)
                else:
                    await statusM.sendOrUpdate()
            await asyncio.sleep(10)
            print("asyncMessage-heartbeat")

    async def registerStatusMessage(self,report):
        message = report.message
        #when a message is registered, check for other statusMessages in the channel.
        #delete other messages in the channel (they will be older)
        #store it in list.
        #regularly (every 10 seconds) check list of statusMessages and run their update function.
        async for history in message.channel.history(limit=100):
            if history.author == self.user and history != message:
                if re.match(r'\*\*Information requested:\*\* Service status',history.content):
                    print("FOUND a definite message\t%s" % (history.content))
                    await history.delete()
                    #    self._statusMessages.remove(history)
        self._statusMessages.append(report)
        
    async def reactivateHistoricStatusMessages(self):
        for guild in self.guilds:
            for channel in guild.channels:
                if channel.type.name == "text":
                    try: 
                        async for history in channel.history(limit=100):
                            if history.author == self.user:
                                if re.match(r'\*\*Information requested:\*\* Service status',history.content):
                                    print("FOUND a definite message\t%s" % (history.content))
                                    deadStatusMessage = models.statusMessage.statusMessage(channel,message=history)
                                    self._statusMessages.append(deadStatusMessage)                            
                    except Exception as e:
                        print("ERROR in reactivating historical status messages -\t%s\n%s"% (channel.name,e))

                                

    
    async def on_message(self,message):
         
        selfID = self.user.id
        if message.author.id != selfID: #recursion check. do not react to your own messages
                
            
            regexText = r'(!0071?8?2?7?4?6?0?2? |\/0071?8?2?7?4?6?0?2? ){1}([a-zA-Z0-9 ]*){1}(-[a-zA-z]*)?' 
            if re.search(r'[!?/](0071?8?2?7?4?6?0?2? )?valh[ei]{2}m', message.content):
                await handlers.cmdValheim(message,self.serviceMonitorInstance,self)
            elif re.search(r'[!?/](0071?8?2?7?4?6?0?2? )?a?waken?', message.content):
                await handlers.cmdAwaken(message,self)
            elif re.search(regexText,message.content):
                pieces = re.split(regexText,message.content)
                await handlers.cmdGeneral(message,pieces,self)
            elif message.guild is None: 
                regexText = r'([a-zA-Z0-9 ]*){1}(-[a-zA-z]*)?'
                if re.search(regexText,message.content):
                    pieces = re.split(regexText,message.content)
                    pieces = ['','',pieces[1],pieces[2], '']
                    await handlers.cmdGeneral(message,pieces,self)

            elif re.search(r'(00718274602)',message.content):
                await handlers.reactTrophies(message)
            elif re.search(r'(007[0-9]*)',message.content):
                await handlers.reactEyes(message)
            

    
    async def on_ready(self):

        
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    

        self.serviceMonitorInstance = await serviceMonitor.getActiveMonitor()
        self.statusUpdaterLoop = threading.Thread(target=self.serviceUpdaterLoop)
        self.statusUpdaterLoop.start()
        self.loop.create_task(self.updateStatusMessagesLoop())
        await self.reactivateHistoricStatusMessages()
        

if __name__ == "__main__":
    bot = Warforged()
    with open("auth.json",'r') as json_file:
        config = json.load(json_file)
    bot.run(config['token'])


