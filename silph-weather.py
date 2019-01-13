import discord
from discord.ext import commands
import pyowm
from geopy.geocoders import Nominatim
import urllib.request
import os

# Get stuff for converting between UTC to localtime
from datetime import datetime
from pytz import timezone
import pytz
from tzwhere import tzwhere

print('Setting up timezone stuff...')
tzwhere = tzwhere.tzwhere()
utc = pytz.utc

print('Setting up location stuff...')
geolocator = Nominatim()

    #prefix
print('Seting up bot and OWM...')
bot = commands.Bot(command_prefix='% ')
owm = pyowm.OWM('OWM CODE')


@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-----RUNNING-----')
	#server list				 
	servers=list(bot.servers)
	print("Connected on" + str(len(bot.servers)) + "servers:")
	for x in range(len(servers)):
		print(' '+servers[x-1].name)
	#bot is playing a game
	await bot.change_presence(game=discord.Game(name='v0.2.5'))
	
	print('-----DONE-----')


#-------------
#utility functions
#-------------
def degToCompass(num):
    val = int((num/22.5)+.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]

def utcToLocal(latitude, longitude, UTC):
    utc_dt = utc.localize(datetime.utcfromtimestamp(UTC))
    local_tz = timezone(tzwhere.tzNameAt(latitude, longitude))

    #print(local_tz)

    local_time = utc_dt.astimezone(local_tz)
    return local_time

#-------------
#bot commands
#-------------

        #help - one tab between command and info

bot.remove_command("help")

@bot.command(pass_context=True)
async def help(ctx):
    await bot.say(" ``` help	       Shows this message. \n w Location	 Shows current weather for location \n f Location     Shows a forcast for the location \n r Location	 Shows current radar for location radar \n % invite	   Creates bot invite link \n ping	       Shows creators of bot ``` ")

        #invite
@bot.command(pass_context=True)
async def invite(ctx):
    await bot.say("https://discordapp.com/api/oauth2/authorize?client_id=388931719417430016&permissions=1141369936&scope=bot")
	


        #ping
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("Created by TxJacob and ADeafBlindMan")


        #!unleashholyterror
@bot.command(pass_context=True)
async def unleashholyterror(ctx):
    await bot.say(":fire::raised_hand_with_fingers_splayed::pray::church::mosque::synagogue::fire:")

        #unleashthekracken
@bot.command(pass_context=True)
async def unleashthekracken(ctx):
    await bot.say(":squid:")

         #bark
@bot.command(pass_context=True)
async def bark(ctx):
    await bot.say("<:bulba:423336927177998346>")

		#order66
@bot.command(pass_context=True)
async def order66(ctx):
        await bot.say("https://pbs.twimg.com/media/DK_Tw9wUEAE7V8_.jpg")


        #weather
@bot.command(pass_context=True)
async def w(ctx, *args):

    ## Join all the strings given.
    string = ' '.join(args)

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
        msg.add_field(name = "Wind", value =  degToCompass(wind["deg"]) + ' ' + str(wind_mph) + " MPH", inline = False) ## Need to fix this line for cases where there is no wind direction.
        msg.add_field(name = "Cloud Coverage", value =  str(cloud_cov) + " %", inline = False)
        msg.add_field(name = "Humidity", value =  str(humidity) + " %", inline = False)
        ## msg.add_field(name = "Code", value =  str(wx_code), inline = False)

        ## Clear conditions
        if(wx_code == 800):
            msg.add_field(name = "Boosted Types", value = "<:Grass:429035991349723147> <:Fire:429035989202108418> <:Ground:429035989714075648>", inline = False)
        ## Partly Cloudy
        elif(wx_code == 801 or wx_code == 802 or wx_code == 701):
            msg.add_field(name = "Boosted Types", value = "<:Normal:429035989898362900> <:Rock:429035989491777538>", inline = False)
        ## Cloudy
        elif(wx_code == 803 or wx_code == 804 or wx_code == 721):
            msg.add_field(name = "Boosted Types", value = "<:Fairy:429035990028386306> <:Fighting:429035989256765452> <:Poison:429035991345528832>", inline = False)
        ## Fog
        elif(wx_code == 741):
            msg.add_field(name = "Boosted Types", value = "<:Dark:429035989437120512> <:Ghost:429035991211311115>", inline = False)
        ## Rain
        elif(wx_code >= 200 and wx_code < 600):
            msg.add_field(name = "Boosted Types", value = "<:Water:429035989571207170> <:Electric:429035989613150208> <:Bug:429035988875214849>", inline = False)
        ## Wind
        elif(wx_code >= 952 and wx_code < 958):
            msg.add_field(name = "Boosted Types", value = "<:Flying:429035989692973056> <:Dragon:429035989336588298> <:Psychic:429035991521558528>", inline = False)
        ## Snow
        elif(wx_code >= 600 and wx_code < 700):
            msg.add_field(name = "Boosted Types", value = "<:Ice:429035989487321090> <:Steel:429035991127425025>", inline = False)

        await bot.send_message(ctx.message.channel, embed = msg)

    ## If the location is not found alert the user.
    except pyowm.exceptions.not_found_error.NotFoundError:
        await bot.say("Location not found!")

@bot.command(pass_context=True)
async def f(ctx, *args):

    ## Join all the strings given.
    string = ' '.join(args)

    location = geolocator.geocode(string)

    w, h = 8, 27;
    data = [[0 for x in range(w)] for y in range(h)]

    try:
        ## Get the weather
        forecast = owm.three_hours_forecast_at_coords(location.latitude, location.longitude)
        f = forecast.get_forecast()

        ## Iterate through the forecast hours and print information
        w_lst = f.get_weathers()
        for n in range(0,27):
            weather = w_lst[n]

            time = utcToLocal(location.latitude, location.longitude, weather.get_reference_time())
            temp = weather.get_temperature(unit = 'fahrenheit')
            cloud_coverage = weather.get_clouds()
            wind = weather.get_wind()
            wx_code = weather.get_weather_code()

            ## Create a 2d list of the parsed weather data
            data[n][0] = time.strftime('%A')
            data[n][1] = time.strftime('%H:%M')

            ## Clear conditions
            if(wx_code == 800):
                data[n][2] = ":sunny:"
            ## Partly Cloudy
            elif(wx_code == 801 or wx_code == 802 or wx_code == 701):
                data[n][2] = ":white_sun_cloud:"
            ## Cloudy
            elif(wx_code == 803 or wx_code == 804 or wx_code == 721):
                data[n][2] = ":cloud:"
            ## Fog
            elif(wx_code == 741):
                data[n][2] = "<:fog~1:414501765270994959>"
            ## Rain
            elif(wx_code >= 200 and wx_code < 600):
                data[n][2] = ":cloud_rain:"
            ## Wind
            elif(wx_code >= 952 and wx_code < 958):
                data[n][2] = "wind"
            ## Snow
            elif(wx_code >= 600 and wx_code < 700):
                data[n][2] = ":snow:"

            data[n][3] = str(temp["temp"])

        msg = discord.Embed(title= "Forecast for " + str(location), color=0xDF4D11)
        for nn in range(0,26):
            if(data[nn][0] == data[nn+1][0]):
                msg.add_field(name = data[nn][0] + " " + data[nn][1], value = data[nn][2] + " " + data[nn][3] + "°F", inline = True)
            else:
                msg.add_field(name = data[nn][0] + " " + data[nn][1], value = data[nn][2] + " " + data[nn][3] + "°F", inline = True)
                await bot.send_message(ctx.message.channel, embed = msg)
                msg = discord.Embed(title= "Forecast for " + str(location), color=0xDF4D11)


    ## If the location is not found alert the user.
    except pyowm.exceptions.not_found_error.NotFoundError:
        await bot.say("Location not found!")

		
		#radar
@bot.command(pass_context=True)
async def r(ctx, *args):

    wunder_api = "API CODE"

    ## Join all the strings given.
    string = ' '.join(args)

    location = geolocator.geocode(string)

    url = "http://api.wunderground.com/api/" + wunder_api + "/radar/image.gif?centerlat=" + str(location.latitude) + "&centerlon=" + str(location.longitude) + "&radius=100&width=280&height=280&newmaps=1"

    image_path, headers = urllib.request.urlretrieve(url)
    os.rename(image_path, image_path + ".gif")
    await bot.send_file(ctx.message.channel, image_path + ".gif")
    os.remove(image_path + ".gif")
	
	


	
	
#---------
#bot TOKEN
#---------

bot.run('DISCORD TOKEN') # Weather Bot

