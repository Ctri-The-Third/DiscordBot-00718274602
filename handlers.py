import discord
import asyncio
import platform
import math
import random
import re
from models.statusMessage import *
from SQLconnector import * 
import serviceMonitors.serviceValheim
async def reactEyes(message):
    try:
        await message.add_reaction('\N{EYES}')
    except discord.HTTPException:
        pass

async def reactTrophies(message):
    try:
        await message.add_reaction('\N{TROPHY}')
        await message.add_reaction('👍') 
    except discord.HTTPException:
        pass

async def cmdValheim(message,bot, all = None):
    serviceController = bot.serviceMonitorInstance
    if serviceController is None:
        message.channel.send("Unable to connect to service controller - try again in 2 seconds.")
        return
    foundServices = False
    for service in serviceController.getServices(serviceType="valheim"):
        if isinstance(service,serviceMonitors.serviceValheim.ServiceValheim):
            if await service.tryStartService(guild = message.guild):
                foundServices = True
    if foundServices == True:
        await message.channel.send("Attempted to activate appropriate valheim servers. See `!007 status` for progress.")
    else:
        await message.channel.send("No valheim services can be activated from this discord server, have the administrator check `services.json`")

async def cmdAwaken(message, bot):
    computerServices = bot.serviceMonitorInstance.getServices(serviceType = 'server')
    for service in computerServices:
        await service.tryStartService()

async def cmdGeneral(message, pieces, bot):
    try:
        invocation = pieces[1]
        command = pieces[2]
        parameter = pieces[3]
    except:
        invocation = ""
        command = ""
        parameter = ""
        await message.channel.send('`An error has been encountered. Request not processed`')

    if command.lower() == "status":
        await cmdStatus(message,bot)
    elif command.lower() == "help":
        await cmdHelp(message)
    elif command.lower() == "ping":
        await cmdPing(message,bot)
    elif command.lower() == "valheim":
        await cmdValheim(message,bot)
    else:
        await cmdNotFound(message)
    

async def cmdStatus(message,bot):
    report = statusMessage(channel=message.channel)
    await report.sendOrUpdate()
    await bot.registerStatusMessage(report)
    #await bot.updateStatusMessages()
    
    
async def cmdPing(message,bot):
    content = """> Guild - `%s`, %s\n> Channel - `%s`, %s\n> you - `%s`, %s\n> your message - `%s` """ % (message.guild.id, message.guild.name, message.channel.id, message.channel.type.name, message.author.id, message.author.display_name, message.id )
    await message.channel.send(content)


async def cmdHelp(message):
    msg = await message.channel.send('''Greetings. This bot primarily serves to monitor the status of services and servers. Use the following commands to interact with me. If you _must_, the shorthand `!007` will work.
        
You are cleared for the following instructions.
> `!00718274602 status` - Shows the status of all servers and services being monitor
> `!00718274602 awaken`/`wake`/`awake` - Awakens the monitored servers
> `!00718274602 valheim` - activates all valheim game-servers.
\n 
Note that servers and services may shutdown outside of normal "awake" hours if inactive for more than 20 minutes. '''
              
        )
async def cmdNotFound(message):
    msg = await message.channel.send('''Unrecognised or unauthorised request. Try `!00718274602 help`''')
