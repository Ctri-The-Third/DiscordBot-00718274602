#pip install -U git+https://github.com/Rapptz/discord.py
import discord
from discord.ext import commands
import random
import json
import asyncio
import re
import handlers

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event 
async def on_message(message):
    global bot 
    selfID = bot.user.id
    if message.author.id != selfID: #recursion check. do not react to your own messages
            
        
        regexText = r'(!0071?8?2?7?4?6?0?2? |\/0071?8?2?7?4?6?0?2? ){1}([a-zA-Z0-9 ]*){1}(-[a-zA-z]*)?'
        if re.search(regexText,message.content):
            pieces = re.split(regexText,message.content)
            await handlers.cmdGeneral(message,pieces,bot)
        elif message.guild is None: 
            regexText = r'([a-zA-Z0-9 ]*){1}(-[a-zA-z]*)?'
            if re.search(regexText,message.content):
                pieces = re.split(regexText,message.content)
                pieces = ['','',pieces[1],pieces[2], '']
                await handlers.cmdGeneral(message,pieces,bot)

        elif re.search(r'(00718274602)',message.content):
            await handlers.reactTrophies(message)
        elif re.search(r'(007[0-9]*)',message.content):
            await handlers.reactEyes(message)
        

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


with open("auth.json",'r') as json_file:
    config = json.load(json_file)
bot.run(config['token'])
