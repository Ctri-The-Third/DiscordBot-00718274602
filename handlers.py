import discord
import asyncio
import platform
import math
import random
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

async def cmdValheim(message,serviceController,bot):
    if serviceController is None:
        message.channel.send("Unable to connect to service controller - try again in 2 seconds.")
        return
    for service in serviceController.getServices():
        if isinstance(service,serviceMonitors.serviceValheim.ServiceValheim):
            await service.tryStartService()
            await message.channel.send("Attempting to activate %s. See `!007 status` for server status." % service.getFriendlyName())
        elif isinstance (service,serviceMonitors.serviceComputer.ServiceComputer):
            await service.tryStartService()
            await message.channel.send("Sending awake instruction to %s. NOTE: run this again once it's woken up!")


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
    elif command.lower() == "redact":
        await cmdRedact(message,bot)
    elif command.lower() == "help":
        await cmdHelp(message)
    elif command.lower() == "historical":
        await cmdHistorical(message)
    elif command.lower() == "morning" or command.lower() == "good morning":
        await cmdMorning(message)
    elif command.lower() == "ping":
        await cmdPing(message,bot)
    else:
        await cmdNotFound(message)
    

async def cmdStatus(message,bot):
    report = statusMessage(channel=message.channel)
    await report.sendOrUpdate()
    await bot.registerStatusMessage(report)
    #await bot.updateStatusMessages()
    
    
async def cmdPing(message,bot):
    content = """> Channel - %s,%s\n> you - %s,%s\n> your message - %s """ % (message.channel.id, message.channel.type.name, message.author.id, message.author.display_name, message.id )
    await message.channel.send(content)


async def cmdRedact(message, bot):

#    msg = await message.channel.send('This message will self destruct in 3 seconds ')
#    
#    await asyncio.sleep(3.0)
#    await msg.edit(content='`[DATA REDACTED]`')
#    await asyncio.sleep(3.0)
#    await msg.edit(content='`[████ ████████]`')
#    await asyncio.sleep(30.0)
#    await msg.delete()
    counter = 0
    async for msg in message.channel.history(limit=7):
        
        if msg.author.id == bot.user.id or msg.id == message.id:
            try: 
                await msg.delete()
                counter = counter + 1
            except:
                pass
        #print(msg)
    await message.channel.send("Expunged %s messages" % counter)


async def cmdHelp(message):
    msg = await message.channel.send('''Thank you for contacting █████ ████████ for assistance. 
Unfortunately you are not authorised to receive assistance from ███ ████ resources. 
Remain Calm.
        
You are cleared for the following instructions.
> `!00718274602 morning` - a standard greeting.
> `!00718274602 redact` - this command removes classified messages from the public domain.
> `!00718274602 status` - This command details recent activities within the ███████ application. 
> `!00718274602 help` - displays this message.
> `!00718274602 historical` - briefly retells a incident report from the █████ ████████
\n at this time direct conversations are ███ monitored by ███ ████. '''
              
        )
async def cmdNotFound(message):
    msg = await message.channel.send('''Unrecognised or unauthorised request. Try `!00718274602 help`''')

async def cmdHistorical(message):
    text = '''Did you ever ████ the ███████ of █████ ████████ The ████? 
I thought not. It’s not a █████ ███ ████ would ████ you.
It’s a ████ legend. █████ ████████ was a ████ ████ of ███ ████, so powerful and so wise ██ could use the █████ to █████████ the █████████████ to create ████… 
██ had such a knowledge of ███ ████ ████ that ██ could even keep the ones ██ cared about from █████. 
███████████████████████████████████████████████████████████████████████████████████████. 
██ became so powerful… the only thing ██ was ██████ of was losing ███ power, which eventually, of course, ██ ███. 
Unfortunately, ██ ██████ ███ ██████████ everything ██ knew, then ███ apprentice killed ███ in ███ █████. 
Ironic. ██ could ████ others from █████, but not ███████.'''
    msg = await message.channel.send(text)
    await asyncio.sleep(10.0)
    await msg.delete()

async def cmdMorning(message):
    embed = discord.Embed()
    embed.title = "Greeting"
    embed.set_footer(text="NOTE: This greeting does not imply exceptional familiarity.")
    additionalcomments = ["Weather based observations","Comment regarding frequency of public transportation"]
    
    max = len(additionalcomments)
    addtionalComment = additionalcomments[random.randint(0,max-1)]


    embed.add_field(name="greeting value",value="basic", inline=True)
    embed.add_field(name="familiarity index", value="distant",inline = True)
    embed.add_field(name="additional comments",value =addtionalComment, inline = False)
    


    embed.description = "This represents a single unity of recognition and good will with the parameters listed below."
    msg = await message.channel.send("Good morning %s, please find your greeting attached." % message.author.mention, embed=embed)
    