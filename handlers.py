import discord
import asyncio
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



async def cmdGeneral(message, pieces):
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
        await cmdRedact(message)
    elif command.lower() == "help":
        await cmdHelp(message)
    elif command.lower() == "historical":
        await cmdHistorical(message)
    else:
        await cmdNotFound(message)
    

async def cmdStatus(message):
    await message.channel.send('**Bot Status: **`Active`\t ✅')

    try:
        conn = connectToSource()
        
        cursor = conn.cursor()
        sql = """ with data as (select row_number() over (partition by healthstatus order by finished desc ) as row, * from public."jobsView")
        select * from data where finished is null or (finished is not null and row <= 3 and row > 0)
        order by finished desc, started asc"""
        cursor.execute(sql)
        results = cursor.fetchall()
        await message.channel.send('**DB Status: **`Connected`\t ✅')
    except:
        await message.channel.send('**DB Status: **`Disabled`\t ❌')
        
    outStr = ""
    for result in results:
        outStr = outStr + "> %s\t%s\t%s   %s \n" % (result[4][-5:],result[1],result[3],result[7]) 
    outStr = "Active and recent DB jobs \n```%s```" % (outStr)
    await message.channel.send(outStr)



async def cmdRedact(message):

    msg = await message.channel.send('This message will self destruct in 3 seconds ')
    await asyncio.sleep(3.0)
    await msg.edit(content='[DATA REDACTED]')
    await asyncio.sleep(3.0)
    await msg.edit(content='[████ ████████] ')
    await asyncio.sleep(30.0)
    await msg.delete()

async def cmdHelp(message):
    msg = await message.channel.send('''Thank you for contacting █████ ████████ for assistance. 
Unfortunately you are not authorised to receive assistance from ███ ████ resources. 
Remain Calm.
        
You are cleared for the following instructions.
> `!00718274602 redact` - this command provides a brief example of proper data redaction processes.
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
