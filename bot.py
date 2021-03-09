#pip install -U git+https://github.com/Rapptz/discord.py
import discord
import random
import json
import asyncio
import re
import handlers

class Warforged(discord.Client):
    
    _statusMessages = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.statusUpdaterLoop = self.loop.create_task(self.statusUpdater())


    async def statusUpdater(self):
        await self.wait_until_ready()
        channel = self.get_channel(689778243225780338) # channel ID goes here
        counter = 0
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(20) # task runs every 60 seconds


    def registerStatusMessage(self,message):

        pass
        #when a message is registered, check for other statusMessages in the channel.
        #delete other messages in the channel (they will be older)
        #store it in list.
        #regularly (every 10 seconds) check list of statusMessages and run their update function.
    

    
    async def on_message(self,message):
         
        selfID = self.user.id
        if message.author.id != selfID: #recursion check. do not react to your own messages
                
            
            regexText = r'(!0071?8?2?7?4?6?0?2? |\/0071?8?2?7?4?6?0?2? ){1}([a-zA-Z0-9 ]*){1}(-[a-zA-z]*)?'
            if re.search(regexText,message.content):
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

if __name__ == "__main__":
    bot = Warforged()
    with open("auth.json",'r') as json_file:
        config = json.load(json_file)
    bot.run(config['token'])


