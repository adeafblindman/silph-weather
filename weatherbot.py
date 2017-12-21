import discord
from discord.ext import commands

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
    await bot.say("i'm alive!")


@bot.command(pass_context=True)
async def w(ctx):
    msg = discord.Embed(title="title", description="description",color=0xDF4D11)
    msg.set_footer(text="footer")
    msg.set_author(name="Author")
    msg.add_field(name="Weather Coming Soon", value="value", inline=True)
    await bot.send_message(ctx.message.channel, embed=msg)
#---------
#bot TOKEN
#---------

bot.run('token')
