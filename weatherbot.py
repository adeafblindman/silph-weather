import discord
from discord.ext import commands
from discord.ext.commands import bot



bot = commands.Bot(command_prefix='!')


@bot.event
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----RUNNING-----')

#-------------
#bot commands
#-------------


@bot.command(pass_context=True)
def ping(ctx):
    await bot.say("i'm alive!")


@bot.command(pass_context=True)
def w(ctx):
    embed = discord.Embed(title="title", description="description",color=0xDF4D11)
    embed.set_footer(text="footer")
    embed.set_author(name="Author")
    embed.add_field(name="Weather Coming Soon", value="value", inline=True)
    await bot.send_message(ctx.message.channel, embed=w)
#---------
#bot TOKEN
#---------

bot.run('token')
