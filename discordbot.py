import discord
import logging
from dateutil.parser import parse
from dateutil.tz import gettz
from pytz import timezone
from time import gmtime, strftime
import pickle

logging.basicConfig(level=logging.CRITICAL)
client = discord.Client()

tzinfos = {"CST": gettz("America/Chicago"), "CDT": gettz("America/Chicago"), "PST": gettz("America/Los Angeles"), "PDT": gettz("America/Los Angeles"), "EST": gettz("America/New York"), "EDT": gettz("America/New York")}

day_fmt = '%b %-d @ '
time_fmt = '%-I.%M%p'
# See https://github.com/dateutil/dateutil/issues/94#issuecomment-133733178
add_default_tz = lambda x, tzinfo: x.replace(tzinfo=x.tzinfo or tzinfo)
EST_tz = gettz("America/New York")

timezone_var = {}

timezone_var = pickle.load( open( "tzdata.p", "rb" ) )


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	# standard list of timezones for given time.
	timezone_var = pickle.load( open( "tzdata.p", "rb" ) )

	if message.content.startswith('!tzlist'):
		try:
			msg = get_converted_times(message.content[8:])
		except Exception as e:
			print(e)
			msg = "Can't parse '" + message.content[3:] + "' sorry 🤖"
		await client.send_message(message.channel, msg)

	if message.content.startswith('!tzregister'):
		#Grab timezone and submitted user. User can only update their own timezone
		msg_list = message.content
		msg_list = msg_list.split()

		test = timezone_convert(msg_list[1])
		if test == 'ERROR':
			msg = "You have selected an invalid timezone. Choices are PST,MST,CST,EST,GMT,GMT+1,GMT+2"
			await client.send_message(message.channel, msg)
		else:
			timezone_var[message.author.id] = msg_list[1]
			# Save file
			pickle.dump( timezone_var, open( "tzdata.p", "wb" ) )
			# Respond to user
			resp = "Request successful <@" + str(message.author.id) + ">"
			await client.send_message(message.channel, resp)

	if message.content.startswith('!tzall'):
		msg_tz = message.content[7:]
		msg_tz = msg_tz.split()
		print(msg_tz)
		try:
			test = timezone_convert(msg_tz[0])
		except:
			msg = "You have not specified any timezone."
			await client.send_message(message.channel, msg)
			return
		if test == 'ERROR':
			msg = "You have selected an invalid timezone. Choices are PST,MST,CST,EST,GMT,GMT+1,GMT+2"
			await client.send_message(message.channel, msg)
		else:
			msg = "Users that belong to the chosen timezone are:"
			for key, value in timezone_var.items():
				if value == msg_tz[0]:
					msg = msg + " <@" + str(key) + ">"
			await client.send_message(message.channel, msg)

	if message.content.startswith('!tz '):
		# Catch exception where user hasn't specified another user
		try:
			tomember = message.mentions[0]
		except Exception as e:
			print(e)
			msg = "You need to specify a user to convert to. Format: !tz <tagged user> <time>"
			await client.send_message(message.channel, msg)

		# Store ID's, timezones and the author
		tomemberID = tomember.id
		tomembertz = timezone_var[tomemberID]
		frommember = message.author
		frommemberID = frommember.id
		frommembertz = timezone_var[frommemberID]
		# Grab the "relevant" bit of the message (e.g. @user time)
		msg_list = message.content[3:]
		msg_list = msg_list.split()
		# Store msg as "time timezone" for conversion. If no time specified, use current.
		try:
			msg = msg_list[1] + " " + frommembertz
		except:
			msg = strftime("%H:%M", gmtime()) + " " + frommembertz
		# Convert time to new timezone
		new_time = convert_time(msg, tomembertz, frommembertz)
		# Only send back message if correct format
		if new_time != 1:
			# Respond to user
			msg = "That time is " + new_time + " for the tagged user"
			await client.send_message(message.channel, msg)
		else:
			msg = "You have selected an invalid timezone. Choices are PST,MST,CST,EST,GMT,GMT+1,GMT+2"
			await client.send_message(message.channel, msg)

def timezone_convert(x):
	# Convert between the acronyms and the text versions
	return {
		'PST': "US/Pacific",
		'MST': "US/Mountain",
		'CST': "US/Central",
		'EST': "US/Eastern",
		'GMT': "Etc/Greenwich",
		'GMT+1': "Europe/Madrid",
		'GMT+2': "Europe/Sofia"
	}.get(x,'ERROR')

def convert_time(msg, tomembertz, frommembertz):
	# format message
	msg = msg.strip().replace('.',':',1)
	# get user's timezone as text version
	usertz = timezone_convert(frommembertz)
	# check for error
	if usertz == 'ERROR':
		return 1
	# get tz for usertz
	usertz = gettz(timezone_convert(frommembertz))
	dt = add_default_tz(parse(msg.upper(), fuzzy=True, tzinfos=tzinfos), EST_tz)
	# get new timezone as text version
	new_tz = timezone_convert(tomembertz)
	# calculate new time
	new_time = dt.astimezone(timezone(new_tz)).strftime(time_fmt).lower()
	return new_time

def get_converted_times(msg):
	print(msg)
	msg = msg.strip().replace('.',':',1)
	dt = add_default_tz(parse(msg.upper(), fuzzy=True, tzinfos=tzinfos), EST_tz)
	print(dt)
	pDt = dt.astimezone(timezone('US/Pacific')).strftime(time_fmt).lower() + " pst"
	mSt = dt.astimezone(timezone('US/Mountain')).strftime(time_fmt).lower() + " mst"
	cDt = dt.astimezone(timezone('US/Central')).strftime(time_fmt).lower() + " cst"
	eDt = dt.astimezone(timezone('US/Eastern')).strftime(time_fmt).lower() + " est"
	gMt = dt.astimezone(timezone('Etc/Greenwich')).strftime(time_fmt).lower() + " gmt"
	day = dt.astimezone(timezone('US/Central')).strftime(day_fmt)
	return day + pDt + " -- " + mSt + "--" + cDt + " -- " + eDt + "--" + gMt

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run('client token here')
