import discord
import asyncio
import platform
import math
import random
from SQLconnector import * 

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
        invocation = pieces[1]
        command = pieces[2]
        parameter = pieces[3]
    except:
        invocation = ""
        command = ""
        parameter = ""
        await message.channel.send('`An error has been encountered. Request not processed`')

    if command.lower() == "status":
        await cmdStatus(message)
    elif command.lower() == "redact":
        await cmdRedact(message,bot)
    elif command.lower() == "help":
        await cmdHelp(message)
    elif command.lower() == "historical":
        await cmdHistorical(message)
    elif command.lower() == "morning" or command.lower() == "good morning":
        await cmdMorning(message)
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
    