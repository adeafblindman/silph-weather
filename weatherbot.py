import discord
from discord.ext import commands
import pyowm
from geopy.geocoders import Nominatim

bot = commands.Bot(command_prefix='!')
owm = pyowm.OWM('')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----RUNNING-----')

#-------------
#utility functions
#-------------
def degToCompass(num):
    val = int((num/22.5)+.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


#-------------
#bot commands
#-------------


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("i'm alive!")


@bot.command(pass_context=True)
async def w(ctx, *args):

    ## Join all the strings given.
    string = ' '.join(args)

    geolocator = Nominatim()
    location = geolocator.geocode(string)

    try:
        ## Get the weather
        observation = owm.weather_at_coords(location.latitude, location.longitude)
        w = observation.get_weather()

        sky_status = w.get_detailed_status()
        temp_f     = w.get_temperature(unit = 'fahrenheit')
        wind       = w.get_wind()
        wind_mph   = round(wind["speed"] * 2.23694, 2)
        cloud_cov  = w.get_clouds()
        humidity   = w.get_humidity()
        wx_code    = w.get_weather_code()

        ## Print the weather.
        msg = discord.Embed(title= "Weather for " + str(location), description = str(sky_status), color=0xDF4D11)
        msg.add_field(name = "Temperature", value = str(temp_f["temp"]) + " F", inline = False)
        msg.add_field(name = "Wind", value =  degToCompass(wind["deg"]) + ' ' + str(wind_mph) + " MPH", inline = False)
        msg.add_field(name = "Cloud Coverage", value =  str(cloud_cov) + " %", inline = False)
        msg.add_field(name = "Humidity", value =  str(humidity) + " %", inline = False)
        msg.add_field(name = "Code", value =  str(wx_code), inline = False)

        if(wx_code == 800):
            msg.add_field(name = "Boosted Types", value = "<:Grass:393253049545654272> <:Fire:393253208849514506> <:Ground:393253254928007176>", inline = False)
        elif(wx_code == 741):
            msg.add_field(name = "Boosted Types", value = "<:Dark:393252566340993030> <:Ghost:393252567158882314>", inline = False)
        elif(wx_code >= 200 and wx_code < 600):
            msg.add_field(name = "Boosted Types", value = "<:Water:393252566294724619> <:Electric:393252566114500608> <:Bug:393252565799665677>", inline = False)
        elif(wx_code >= 952 and wx_code < 958):
            msg.add_field(name = "Boosted Types", value = "<:Flying:393252566378479617> <:Dragon:393252566542057473> <:Psychic:393252566785458178>", inline = False)
        elif(wx_code >= 600 and wx_code < 700):
            msg.add_field(name = "Boosted Types", value = "<:Ice:393252567095836672> <:Steel:393252567221796864>", inline = False)


        await bot.send_message(ctx.message.channel, embed = msg)

    ## If the location is not found alert the user.
    except pyowm.exceptions.not_found_error.NotFoundError:
        await bot.say("Location not found!")

#---------
#bot TOKEN
#---------

bot.run('')
