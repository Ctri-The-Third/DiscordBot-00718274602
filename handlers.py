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
    await message.channel.send('received general instruction.\n`%s`' % pieces)
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