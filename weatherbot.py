import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----RUNNING-----')







@bot.command(pass_context=True)
async def ping(ctx):
	await bot.say("im alive!")






bot.run('DISCORD BOT TOKEN')
