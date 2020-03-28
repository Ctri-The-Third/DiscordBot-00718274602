import datetime

import discord
import asyncio
import platform
import math
import random
import config as cfg
from SQLconnector import * 

breachCounter = 0
reactionemojis = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓','⛎','','','','','','','','','','','', ]
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



async def cmdGeneral(message, pieces, bot):
    try:
        invocation = pieces[1] #!007, !self, or None
        command = pieces[2]  #redact, golem, etc...
        parameter = pieces[3] #-20
    except:
        invocation = ""
        command = ""
        parameter = ""
        await message.channel.send('`An error has been encountered. Request not processed`')

    if command.lower() == "status":
        await cmdStatus(message)
    elif command.lower() == "redact":
        await cmdRedact(message,pieces, bot)
    elif command.lower() == "expunge":
        await cmdExpunge(message,pieces,bot)
    elif command.lower() == "help":
        await cmdHelp(message)
    elif command.lower() == "historical":
        await cmdHistorical(message)
    elif command.lower() == "morning" or command.lower() == "good morning":
        await cmdMorning(message)
    elif command.lower() == "golem":
        await cmdGolemSetup(message, bot)
    elif command.lower() == "warforged":
        await cmdGolemShutdown(message, bot)
    else:
        await cmdNotFound(message)
    

async def cmdStatus(message):

    embed = discord.Embed()
    embed.title = "System status"
    embed.add_field(name = "Bot Status", value = "`Active` ✅", inline=True)
    embed.add_field(name = "Bot Home", value = '`%s`' % platform.node(), inline=True)
    
    try:
        conn = connectToSource()
        
        cursor = conn.cursor()
        sql = """ with data as (
            select row_number() over 
            (
                partition by healthstatus order by finished desc ) as row
                , * from public."jobsView"
            )
            select * from data 
            where finished is null or 
            (finished is not null and row <= 3 and row > 0)
            order by finished desc, started asc"""
        cursor.execute(sql)
        results = cursor.fetchall()
        embed.add_field(name = "DB Status", value = "`Connected` ✅", inline=True)
    except:
        embed.add_field(name = "DB Status", value = "`OFfline` ❌", inline=True)

    await message.channel.send(embed=embed)            
    embed = discord.Embed()
    embed.title = "Active and recent ETL jobs"
    
    
    for result in results:
        statusString = "%s **%s**" %(result[4][-5:],result[1])
        if result[11] is not None:
            statusString = "%s, %s%%" % (statusString, result[11]) 
        embed.add_field(name = statusString, value = "%s" % (result[3]+" "*40)[:40]) 
        completionTime = "%s" %(result[7])
        completionTime = completionTime[0:19]
        embed.add_field(name="Completion time",value = "%s" % (completionTime),inline=True)
        embed.add_field(name="Blocking | Blocked by",value = "0 | 0")
    await message.channel.send(embed=embed)
    
    


async def cmdRedact(message, pieces, bot):

    counter = 0
    newMsg = await message.channel.send("Redacting..." )
    limit = 10

    try:
        limit = int(pieces)
    except Exception as e:
        pass

    
    async for msg in message.channel.history(limit=limit):
        if (msg.author.id == bot.user.id or msg.id == message.id ) and msg.id != newMsg.id :
            try: 
            
                await msg.edit(suppress = True, content = "`[redacted]`")
                #await msg.embeds.Delete()
                counter = counter + 1
            except:
                pass
        #print(msg)
    await newMsg.edit(content = "REDACTED `%s` messages, searched through `%s`" % (counter,limit))    


async def cmdExpunge(message, pieces,bot):
    limit = 10
    counter =0  
    try:
        limit = int(pieces [3])
    except Exception as e:
        pass
    print("trying to expunge %s" %(limit))
    async for msg in message.channel.history(limit=limit):            
        if msg.author.id == bot.user.id or msg.author.id == message.author.id:
                try:         
                    await msg.delete()
                    counter = counter + 1
                except:
                    pass
    await message.channel.send("EXPUNGED `%s` messages, searched through `%s`" % (counter,limit))    
    return

async def cmdGolemSetup(message, bot):
    global reactionemojis
    text = "> **List of all guilds and channels this bot has access to.**\n```"
    counter = 0 
    for guild in bot.guilds:
        text = text + "%s \t %s\n" % (guild.name, guild.id)
        for channel in guild.channels:
            if channel.type.name == "text":
                
                text = text + "[%s]\t%s\t%s\t%s\n" % (reactionemojis[counter], channel.name, channel.id,channel.type.name)
                counter = counter + 1 

    text = text + "```\n> To direct 00718274602 to communicate in a channel, react appropriately. Press [❌] to clear"

    
    msg = await message.channel.send(text)
    otherCounter = 0
    await msg.add_reaction("❌")


    while otherCounter < counter:
        await msg.add_reaction(reactionemojis[otherCounter])
        otherCounter = otherCounter + 1 

    #await msg.add_reaction('🇦')
    #await msg.add_reaction('🇧')    
    return 

async def cmdGolemShutdown(message, bot):
    cfg.golemMode["enabled"] = False
    await message.channel.send('`Golem mode disabled`')


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

async def forbiddenText(message):
    if message.channel.id != 689492668979609812:
        try:
            global breachCounter
            embed = discord.Embed()
            embed.title = "Redaction notice"
            embed.description = "Please be aware that automated security protocols have detected unsanctioned discussion of a classified subject.\nIt is required that conversation on this subject be restricted to authorised locations only."
            today = datetime.datetime.today()
            
            embed.set_footer(text="This breach has been logged, case ID %s%s%s" % (today.month,today.day,breachCounter))
            embed.colour = discord.colour.Colour(15158332)
            await message.channel.send(embed = embed)
            breachCounter = breachCounter + 1
            await message.delete()
            
        except Exception as e:
            print(e)
            pass


async def golemMessage(message,bot):
    if message.channel.id == cfg.golemMode["sourceChannelID"]:
        targetChannel = await bot.fetch_channel(cfg.golemMode["channelID"])
        await targetChannel.send(message.content)
        #if so, route to TARGET channel
    elif message.channel.id == cfg.golemMode["channelID"]:
        sourceChannel = await bot.fetch_channel(cfg.golemMode["sourceChannelID"])
        await sourceChannel.send("%s: %s" % (message.author.name, message.content))
        #if so, route to source channel.
    else:   
        return
        
    #then check if it's in the SOURCE channel
async def reactGolemList(reaction,user,bot):
    #await reaction.message.channel.send("reaction detected to golem scout")
    channelIndex = -1
    if reaction.emoji == "❌":
        await reaction.message.edit (content = "`Golem mode disabled`")
        cfg.golemMode["enabled"] = False
        return

    try: 
        channelIndex = reactionemojis.index(reaction.emoji)
    except Exception as e:
        await reaction.message.channel.send("Reaction not mapped correctly.")
        return    

    else:
        counter = 0
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.type.name == "text":
                    if counter == channelIndex:
                        cfg.golemMode["enabled"] = True
                        cfg.golemMode["channelID"] = channel.id
                        cfg.golemMode["sourceChannelID"] = reaction.message.channel.id
                        #await channel.send("`Communication to channel authorised`")
                        await reaction.message.edit(content = "```golem mode enabled. react with :x: to disable.\nTarget is channel [%s]```" %  (channel.name))
                        
                        break 
                    
                    counter = counter + 1 
        #seekID

    return