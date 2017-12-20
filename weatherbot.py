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

#-------------
#bot commands
#-------------


@bot.command(pass_context=True)
async def ping(ctx):
	await bot.say("im alive!")


@bot.command(pass_context=True)
async def w(ctx):
    embed = discord.Embed(title="title", description="description",color=0xDF4D11)
    embed.set_footer(text="footer")
    embed.set_author(name="Author")
    embed.add_field(name="Weather Coming Soon", value="value", inline=True)
    await bot.say(embed=w)
#---------
#bot TOKEN
#---------

bot.run('token')
