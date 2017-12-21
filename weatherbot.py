import discord
from discord.ext import commands
import pyowm

bot = commands.Bot(command_prefix='!')
owm = pyowm.OWM('')


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
async def w(ctx, *args):

    ## Join all the strings given.
    location = ' '.join(args)

    ## Get the weather
    observation = owm.weather_at_place(location)
    w = observation.get_weather()

    sky_status = w.get_status()
    temp_f = w.get_temperature(unit = 'fahrenheit')
    wind = w.get_wind()
    wind_mph = round(wind["speed"] * 2.23694, 2)

    ## Print the weather.
    msg = discord.Embed(title= "Weather for " + str(location), description = str(sky_status), color=0xDF4D11)
    msg.add_field(name="Temperature", value = str(temp_f["temp"]) + " F", inline=True)
    msg.add_field(name="Wind", value = str(wind_mph) + " MPH", inline=True)
    

    await bot.send_message(ctx.message.channel, embed=msg)
    #await bot.send_message(ctx.message.channel, str(location))

#---------
#bot TOKEN
#---------

bot.run('')
