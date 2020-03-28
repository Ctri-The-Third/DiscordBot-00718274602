#pip install -U git+https://github.com/Rapptz/discord.py
import discord
from discord.ext import commands
import random
import json
import asyncio
import re
import handlers
import config as cfg
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event 
async def on_message(message):
    global bot 
    selfID = bot.user.id

    if message.author.id != selfID: #someone else is invoking 007
            
        if re.search(r'(Coronavirus|covid)+', message.content, flags = re.IGNORECASE):
            await handlers.forbiddenText(message)

        regexText = r'(!0071?8?2?7?4?6?0?2? |\/0071?8?2?7?4?6?0?2? ){1}([a-zA-Z0-9 ]*){1}(-[a-zA-z0-9]*)?'
        if re.search(regexText,message.content):
            pieces = re.split(regexText,message.content)
            await handlers.cmdGeneral(message,pieces,bot)
        elif message.guild is None and message.author.id: 
            regexText = r'([a-zA-Z0-9 ]*){1}(-[a-zA-z]*)?'
            if re.search(regexText,message.content):
                pieces = re.split(regexText,message.content)
                pieces = ['','',pieces[1],pieces[2], '']
                await handlers.cmdGeneral(message,pieces,bot)

        elif re.search(r'(00718274602)',message.content):
            await handlers.reactTrophies(message)
        elif re.search(r'(007[0-9]*)',message.content):
            await handlers.reactEyes(message)




    if message.author.id == selfID and cfg.golemMode["enabled"] == True: #007 is invoking himself (probably via golem mode)
        regexText = r'(!self ){1}([a-zA-Z0-9 ]*){1}(-[a-zA-z0-9]*)?'
        if re.search(regexText,message.content):
            pieces = re.split(regexText,message.content)
            await handlers.cmdGeneral(message,pieces,bot)
    if message.author.id != selfID and cfg.golemMode["enabled"] == True: #golem mode catchall - for feeding messages TO the pilot, and FROM the pilot.
        await handlers.golemMessage(message,bot)
        #additional handlers so 007 self censors
        if re.search(r'(Coronavirus|covid)+', message.content, flags = re.IGNORECASE):
            await handlers.forbiddenText(message)
        


async def checkDB(self):
    await self.wait_until_ready()
    channel = self.get_channel
    while not self.is_closed():
        
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_reaction_add(reaction,user):
    global config
    handlerMethods = []
    handlerMethods.append({"restr" : r'(List of all guilds and channels this bot has access to.)' , "method" : handlers.reactGolemList })
    handlerMethods.append({"restr" : r'(```golem mode enabled\. react with :x: to disable\.)' , "method" : handlers.reactGolemList })
    

    #if reaction.message.author = bot
    if user.id == bot.user.id:
        return
    if reaction.message.author.id == bot.user.id:
        for handler in handlerMethods:
            if re.search(handler["restr"],reaction.message.content):
                await handler["method"](reaction,user,bot)

    #if reaction.message text = regexmatch
        #handlers.reactToScout
    #await reaction.message.channel.send("Reaction detected!")
    return


bot.run(cfg.authToken)


#sock mode - accessible via 1to1 chat
# lists channels
# reaction handler (X)
# embed builder 
# embed preview
# embed send
