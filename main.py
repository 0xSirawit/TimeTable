#Setup
import datetime
import pytz
import json
import discord
from discord import message
from discord import embeds
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands, tasks
from keep_alive import keep_alive

#set variable & etc.
global nchannel,nchannel_id,status_of_notice
nchannel = "-"
nchannel_id = 0
status_of_notice = "disable"
client = commands.Bot(command_prefix = '.')
client.remove_command('help')
TOKEN = "" #bot's token

@client.event
async def on_ready():
  notification.start()
  updates.start()
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="⚙️.helpt"))
  print('logged in as {0.user}'.format(client))  
  
@tasks.loop(seconds=1)
async def updates():
  global daytimetable,color_today,Cmonday,Ctuesday,Cwednesday,Cthursday,Cfriday,today,now_table_embed,next_table_embed,help_embed,now,weekday
  #Set time & update time
  tz_thai = pytz.timezone("Asia/Bangkok")
  now = datetime.datetime.now(tz_thai)
  today = now.strftime("%A")
  weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

  #Read json file 
  myjsonfile=open('Time.json','r')
  jsondata=myjsonfile.read()
  obj=json.loads(jsondata)
  daylist=obj[today]

  #Weekdays colors
  Cmonday = 0xFFFF00
  Ctuesday = 0xFFC0CB
  Cwednesday = 0x00FF00
  Cthursday = 0xFFA500
  Cfriday = 0xADD8E6
  if today == "Monday":color_today=Cmonday
  if today == "Tuesday":color_today=Ctuesday
  if today == "Wednesday":color_today=Cwednesday
  if today == "Thursday":color_today=Cthursday
  if today == "Friday":color_today=Cfriday

  #Order function
  def order():
    order = 0 
    def time_in_range(start, end, current):
      return start <= current <= end
    for i in range(10):
      stimeHR = daylist[i].get("startHR")
      stimeMIN = daylist[i].get("startMIN")
      etimeHR = daylist[i].get("endHR")
      etimeMIN = daylist[i].get("endMIN")
      start = datetime.time(stimeHR, stimeMIN, 0)
      end = datetime.time(etimeHR, etimeMIN, 0)
      current = datetime.time(int(now.strftime("%H")), int(now.strftime("%M")), 0)
      if time_in_range(start, end, current) == True:order = i
    return order
      
  #Embed_discord
  #Now
  now_table_embed = discord.Embed(
    title= "Subject["+str(order())+"] : "+daylist[order()].get("subject"),
    description="Date & Time : "+now.strftime("%c"),
    color= color_today
  )
  now_table_embed.add_field(name='Time',value=(daylist[order()].get("time")),inline=False)
  now_table_embed.add_field(name='Link',value=(daylist[order()].get("link")),inline=False)

  #Next subject
  nextsubject = order()+1
  if order() == 9:nextsubject = order()
  next_table_embed = discord.Embed(
    title= "Subject["+str(nextsubject)+"] : "+daylist[nextsubject].get("subject"),
    description="Date & Time : "+now.strftime("%c"),
    color= color_today
  )
  next_table_embed.add_field(name='Time',value=(daylist[nextsubject].get("time")),inline=False)
  next_table_embed.add_field(name='Link',value=(daylist[nextsubject].get("link")),inline=False)

  #Function daytimetable
  def daytimetable(day, colorday): 
    day_table_embed = discord.Embed(
      title= "TimeTable of "+day,
      description="Date & Time : "+now.strftime("%c"),
      color= colorday
    )
    day_table_embed.add_field(name='Subject',value=(obj[day][0].get("subject")),inline=True)
    day_table_embed.add_field(name='Time',value=(obj[day][0].get("time")),inline=True)
    day_table_embed.add_field(name='Link',value=(obj[day][0].get("link")),inline=True)
    for i in range(10):
      j = i+1
      sum =[]
      subject = (obj[day][j].get("subject"))
      time = (obj[day][j].get("time"))
      link = (obj[day][j].get("link"))
      sum.append(subject)
      sum.append(time)
      sum.append(link)
      mix = " | ".join(sum)
      day_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)
    return day_table_embed
    
  #Help
  help_embed = discord.Embed(
    title= "📃 Commands",
    description="Date & Time : "+now.strftime("%c"),
    color= discord.Colour.teal()
  )
  help_embed.add_field(name='Study now',value=".now",inline=True)
  help_embed.add_field(name='Next Subject',value=".next",inline=True)
  help_embed.add_field(name='Table of Weekday',value="---------------------------------------------",inline=False)
  help_embed.add_field(name='Today',value=".today/.td",inline=True)
  help_embed.add_field(name='Monday',value=".mon",inline=True)
  help_embed.add_field(name='Tuesday',value=".tue",inline=True)
  help_embed.add_field(name='Wednesday',value=".wed",inline=True)
  help_embed.add_field(name='Thursday',value=".thu",inline=True)
  help_embed.add_field(name='Friday',value=".fri",inline=True)
  help_embed.add_field(name='Notice function',value="---------------------------------------------",inline=False)
  help_embed.add_field(name='Status',value=status_of_notice,inline=True)
  help_embed.add_field(name='Channel name',value=nchannel,inline=True)
  help_embed.add_field(name='For set notification CH',value=".set",inline=False)
  help_embed.add_field(name='To enable/disble',value=".nena/.ndis",inline=False)

#notification function
@tasks.loop(minutes=1)
async def notification():
  #notification
  def checktime(checktimeMIN,checktimeHR):
    current1 = datetime.time(int(now.strftime("%H")), int(now.strftime("%M")), 0)
    return current1 == datetime.time(checktimeMIN, checktimeHR, 0)

  if str(status_of_notice) == "enable":
    if today in weekday:
      if (checktime(8,0) or checktime(8,30) or 
          checktime(9,10) or checktime(10,45) or 
          checktime(11,25) or checktime(12,5) or 
          checktime(12,5) or checktime(12,45) or
          checktime(13,40) or checktime(14,20) or
          checktime(15,0)
      ):channel1 = client.get_channel(nchannel_id);await channel1.send(embed=now_table_embed)

#commands
@client.command()
async def nena(ctx):
  if nchannel_id != 0:
    globals()['status_of_notice'] = "enable"
    await ctx.send("Notice function is enable")
  else:
    await ctx.send("You have to use \".set\" before enable the notice function.")

@client.command()
async def ndis(ctx):
  globals()['status_of_notice'] = "disable"
  await ctx.send("Notice function is disable")

@client.command()
async def set(ctx):
  globals()['nchannel'] = ctx.channel
  globals()['nchannel_id'] = ctx.channel.id
  message_notice = "Notification Channel id: " + str(nchannel_id)
  await ctx.send("Succeeded setting Channel notification!")
  await ctx.send(message_notice)

@client.command()
async def now(ctx):
  await ctx.send(embed=now_table_embed)

@client.command()
async def next(ctx):
  await ctx.send(embed=next_table_embed)

@client.command()
async def today(ctx):
  await ctx.send(embed=daytimetable(today, color_today))

@client.command()
async def td(ctx):
  await ctx.send(embed=daytimetable(today, color_today))

@client.command()
async def mon(ctx):
  await ctx.send(embed=daytimetable("Monday", Cmonday))

@client.command()
async def tue(ctx):
  await ctx.send(embed=daytimetable("Tuesday", Ctuesday))

@client.command()
async def wed(ctx):
  await ctx.send(embed=daytimetable("Wednesday", Cwednesday))

@client.command()
async def thu(ctx):
  await ctx.send(embed=daytimetable("Thursday", Cthursday))

@client.command()
async def fri(ctx):
  await ctx.send(embed=daytimetable("Friday", Cfriday))

@client.command()
async def helpt(ctx):
  await ctx.send(embed=help_embed)

keep_alive()
client.run(TOKEN)
