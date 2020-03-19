#pip install -U git+https://github.com/Rapptz/discord.py@rewrite
import discord
from discord.ext import commands
import random
import json
import asyncio
import re

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event 
async def on_message(message):

    if message.content.startswith('!007 redact'):
        try:
            await message.add_reaction('\N{EYES}')
        except discord.HTTPException:
            pass
        msg = await message.channel.send('This message will self destruct in 3 seconds ')
        await asyncio.sleep(3.0)
        await msg.edit(content='[DATA REDACTED]')
        await asyncio.sleep(3.0)
        await msg.edit(content='[████ ████████] ')
        await asyncio.sleep(30.0)
        await msg.delete()
    if re.search(r'(007[0-9]*)',message.content):
        try:
            await message.add_reaction('\N{EYES}')
        except discord.HTTPException:
            pass
    if re.search(r'(00718274602)',message.content):
        try:
            await message.add_reaction('\N{TROPHY}')
            await message.add_reaction('👍') 
        except discord.HTTPException:
            pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


with open("auth.json",'r') as json_file:
    config = json.load(json_file)
bot.run(config['token'])
