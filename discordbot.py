import discord
import logging
from dateutil.parser import parse
from dateutil.tz import gettz
import pytz
from time import gmtime, strftime
import datetime
from random import *

# Defines "now"
now = datetime.datetime.now()
# Discord setup
logging.basicConfig(level=logging.CRITICAL)
client = discord.Client()
# Time format
time_fmt = '%-I.%M%p'

# Repository and adapter setup
timezone_var = {}
from repository import Repository
from adapters.legacy_adapter import LegacyAdapter
timezone_var = Repository(LegacyAdapter())

@client.event
async def on_message(message):
    # Stop bot replying to itself
    if message.author == client.user:
        return
    # standard list of timezones for given time.
    timezone_var = Repository(LegacyAdapter())

    # sass module activated - on a random message gen a random number between 1 and 50
    # If it's 24 - tell them that nobody cares.
    if randint(1, 50) == 24:
        print("Told somebody to shut up")
        msg = "<@" + str(message.author.id) + "> shhhhhh - nobody cares!"
        await client.send_message(message.channel, msg)

    if message.content.startswith('!tzlist'):
        # Provides list of timezones and conversions
        try:
            if len(message.content) < 14:
                msg = "No timezone was included. Defaulting to GMT"
                await client.send_message(message.channel, msg)
            msg = get_converted_times(message.content[8:])
        except Exception as e:
            print(e)
            msg = "Can't parse '" + message.content[8:] + "' sorry 🤖"
        await client.send_message(message.channel, msg)

    # Registers user to timezone
    if message.content.startswith('!tzregister'):

        # Ensure user specifies timezone
        if len(message.content) < 13:
            msg = "No timezone specified. Usage: !tzregister <timezone>"
            await client.send_message(message.channel, msg)

        #Grab timezone and submitted user. User can only update their own timezone
        msg_list = message.content
        msg_list = msg_list.split()

        # Error catching
        test = timezone_convert(msg_list[1])
        if test == 'ERROR':
            msg = "You have selected an invalid timezone. Choices are PST,MST,CST,EST,GMT,GMT+1,GMT+2"
            await client.send_message(message.channel, msg)
        else:
            # Store value
            timezone_var[message.author.id] = msg_list[1]
            # Save file
            timezone_var.store()
            # Respond to user
            resp = "Timezone Registration Successful <@" + str(message.author.id) + ">"
            await client.send_message(message.channel, resp)

    # Show all users belonging to a particular timezone
    if message.content.startswith('!tzall'):
        # Grab timezone
        msg_tz = message.content[7:]
        msg_tz = msg_tz.split()
        # Test timezone exists
        try:
            test = timezone_convert(msg_tz[0])
        except:
            # Get user to specify timezone
            msg = "You have not specified any timezone. Usage: !tzall <timezone>"
            await client.send_message(message.channel, msg)
            return
        # Error checking
        if test == 'ERROR':
            # Invalid timezone
            msg = "You have selected an invalid timezone. Choices are PST,MST,CST,EST,GMT,GMT+1,GMT+2"
            await client.send_message(message.channel, msg)
        else:
            # Valid timezone
            msg = "Users that belong to the chosen timezone are:"
            # Scan for users belonging to timezone
            for key, value in timezone_var.items():
                if value == msg_tz[0]:
                    msg = msg + " <@" + str(key) + ">"
            # Respond to user
            await client.send_message(message.channel, msg)

    # Main timezone adjusting part
    if message.content.startswith('!tz '):
        # Catch exception where user hasn't specified another user
        try:
            tomember = message.mentions[0]
        except Exception as e:
            print(e)
            msg = "You need to specify a user to convert to - make sure they are tagged! Usage: !tz <tagged user> <time>"
            await client.send_message(message.channel, msg)

        # Store ID's, timezones and the author
        tomemberID = tomember.id
        tomembertz = timezone_var[tomemberID]
        frommember = message.author
        frommemberID = frommember.id
        frommembertz = timezone_var[frommemberID]

        # Grab the "relevant" bit of the message (e.g. "@user <time>")
        msg_list = message.content[3:]
        msg_list = msg_list.split()
        # Store msg as "<time> <timezone>" for conversion. If no time specified, use current.
        try:
            msg = msg_list[1] + " " + frommembertz
        except:
            msg = strftime("%H:%M", gmtime())

        # Convert time to new timezone
        new_time = convert_time(msg, tomembertz, frommembertz)

        # Only send back message if correct format
        if new_time != 1:
            # Respond to user
            print("Conversion complete.")
            print("------")
            msg = "That time is " + new_time + " for the tagged user"
            await client.send_message(message.channel, msg)
        else:
            msg = "You have not registered your own timezone. Please use !tzregister"
            await client.send_message(message.channel, msg)

def timezone_convert(x):
    # Convert between the acronyms and the text versions
    return {
        'PST': 'US/Pacific',
        'MST': 'US/Mountain',
        'CST': 'US/Central',
        'EST': 'US/Eastern',
        'GMT': 'Europe/London',
        'GMT+1': 'Europe/Madrid',
        'GMT+2': 'Europe/Sofia'
    }.get(x,'ERROR')

def convert_time(msg, tomembertz, frommembertz):
    # format message
    msg = msg.strip().replace('.',':',1)
    # Adds the current date to the message
    time_with_date = now.strftime("%y-%m-%d") + " " + msg[:5]

    # Converts string to timezone naive time
    time_unaware = datetime.datetime.strptime(time_with_date, '%y-%m-%d %H:%M')

    # If time is omitted off the command, set the timezone as Europe/London (local time for pc)
    # CHANGE THIS PARAMETER TO MATCH YOUR LOCATION
    if len(msg) < 6:
        fromtz = pytz.timezone('Europe/London')
    else:
        # get user's timezone as full text (e.g. EST -> US/Eastern)
        fromtz = timezone_convert(frommembertz)
        # check for error
        if fromtz == 'ERROR':
            return 1
        # Set timezone
        fromtz = pytz.timezone(fromtz)

    # get target's timezone as full text (e.g. EST -> US/Eastern)
    totz = timezone_convert(tomembertz)
    # check for error
    if totz == 'ERROR':
        return 1
    # Set timezone
    totz = pytz.timezone(totz)

    # make time timezone aware
    time_aware = fromtz.localize(time_unaware)

    # Convert user's time to target's timezone
    converted = time_aware.astimezone(totz)
    # Format
    converted = converted.strftime(time_fmt).lower()
    return converted

def get_converted_times(msg):
    # format message
    msg_list = msg.split()
    # Change message depending on specified parameters
    if len(msg_list) == 1:
        msg = msg_list[0] + " GMT"
        frommembertz = "GMT"
    elif len(msg_list) == 2:
        msg = msg_list[0] + " " + msg_list[1]
        frommembertz = msg_list[1]
    elif len(msg_list) == 0:
        msg = "No time was specified. Usage: !tzlist <time> <timezone>"
        return msg
    else:
        msg = "Too many arguments were included. Usage: !tzlist <time> <timezone>"
        return msg

    # Start conversion into timezones
    conv_pst = convert_time(msg, "PST", frommembertz)
    # Invalid timezone error. Only needs checking once for frommembertz - all others are explicit
    if conv_pst == 1:
        msg = "Invalid timezone. Choices are PST,MST,CST,EST,GMT,GMT+1,GMT+2"
        return msg
    conv_mst = convert_time(msg, "MST", frommembertz)
    conv_cst = convert_time(msg, "CST", frommembertz)
    conv_est = convert_time(msg, "EST", frommembertz)
    conv_gmt = convert_time(msg, "GMT", frommembertz)
    conv_gmta = convert_time(msg, "GMT+1", frommembertz)
    conv_gmtb = convert_time(msg, "GMT+2", frommembertz)
    return "PST: " + conv_pst + " -- " + "MST: " + conv_mst + "--" + "CST: " + conv_cst + " -- " + "EST: " + conv_est + "--" + "GMT: " + conv_gmt + "--" + "GMT+1: " + conv_gmta + "--" + "GMT+2: " + conv_gmtb

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('- client token goes here -')
