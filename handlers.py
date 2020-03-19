import discord
import asyncio


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


async def cmdRedact(message):

    msg = await message.channel.send('This message will self destruct in 3 seconds ')
    await asyncio.sleep(3.0)
    await msg.edit(content='[DATA REDACTED]')
    await asyncio.sleep(3.0)
    await msg.edit(content='[████ ████████] ')
    await asyncio.sleep(30.0)
    await msg.delete()