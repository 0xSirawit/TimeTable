#setup
import discord
import json
from datetime import datetime
import pytz
from discord import message
from discord import embeds
from discord.colour import Color
from discord.embeds import Embed
client = discord.Client()
TOKEN="" #bot's token

#main
@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #set time & order of timetable
    tz_thai = pytz.timezone("Asia/Bangkok")
    now = datetime.now(tz_thai)
    today = now.strftime("%A")

    #read json file 
    myjsonfile=open('Time.json','r')
    jsondata=myjsonfile.read()
    obj=json.loads(jsondata)
    daylist=obj[today]
    daymonlist=obj["Monday"]
    daytuelist=obj["Tuesday"]
    daywedlist=obj["Wednesday"]
    daythulist=obj["Thursday"]
    dayfrilist=obj["Friday"]

    #weekday colors
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

    #orderfunction
    def order():
      order = 9
      if now.hour <= 8 and now.minute - 30 < 0:order=0 
      if now.hour == 8 and now.minute - 30 >= 0:order=1 
      if now.hour == 9 and now.minute - 20 <  0:order=1 
      if now.hour == 9 and now.minute - 20 >= 0:order=2 
      if now.hour == 10 and now.minute - 10 < 0:order=2 
      if now.hour == 10 and now.minute - 10 >=0:order=3 
      if now.hour == 11 and now.minute - 50 < 0:order=4 
      if now.hour == 11 and now.minute - 50 >=0:order=5 
      if now.hour == 12 and now.minute - 40 < 0:order=5 
      if now.hour == 12 and now.minute - 40 >=0:order=6 
      if now.hour == 13 and now.minute - 30 <= 0:order=6 
      if now.hour == 13 and now.minute - 30 > 0:order=7 
      if now.hour == 14 and now.minute - 20 < 0:order=7 
      if now.hour == 14 and now.minute - 20 >=0:order=8 
      if now.hour == 15 and now.minute - 10 < 0:order=8 
      if now.hour == 15 and now.minute - 10 >=0:order=9
      return order

    #embed_discord
    now_table_embed = discord.Embed(
        title= "Subject["+str(order())+"] : "+daylist[order()].get("subject"),
        description="Date & Time : "+now.strftime("%c"),
        color= color_today
    )
    now_table_embed.add_field(name='Time',value=(daylist[order()].get("time")),inline=False)
    now_table_embed.add_field(name='Link',value=(daylist[order()].get("link")),inline=False)

    today_table_embed = discord.Embed(
        title= "TimeTable of "+today,
        description="Date & Time : "+now.strftime("%c"),
        color= color_today
    )
    today_table_embed.add_field(name='Subject',value=(daylist[0].get("subject")),inline=True)
    today_table_embed.add_field(name='Time',value=(daylist[0].get("time")),inline=True)
    today_table_embed.add_field(name='Link',value=(daylist[0].get("link")),inline=True)
    for i in range(9):
        j = i+1
        sum =[]
        subject = (daylist[j].get("subject"))
        time =(daylist[j].get("time"))
        link = (daylist[j].get("link"))
        sum.append(subject)
        sum.append(time)
        sum.append(link)
        mix = " | ".join(sum)
        today_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)

    #mon
    mon_table_embed = discord.Embed(
        title= "TimeTable of "+ "Monday",
        description="Date & Time : "+now.strftime("%c"),
        color= Cmonday
    )
    mon_table_embed.add_field(name='Subject',value=(daymonlist[0].get("subject")),inline=True)
    mon_table_embed.add_field(name='Time',value=(daymonlist[0].get("time")),inline=True)
    mon_table_embed.add_field(name='Link',value=(daymonlist[0].get("link")),inline=True)
    for i in range(9):
        j = i+1
        sum =[]
        subject = (daymonlist[j].get("subject"))
        time =(daymonlist[j].get("time"))
        link = (daymonlist[j].get("link"))
        sum.append(subject)
        sum.append(time)
        sum.append(link)
        mix = " | ".join(sum)
        mon_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)
    
    #tue
    tue_table_embed = discord.Embed(
        title= "TimeTable of "+ "Tuesday",
        description="Date & Time : "+now.strftime("%c"),
        color= Ctuesday
    )
    tue_table_embed.add_field(name='Subject',value=(daytuelist[0].get("subject")),inline=True)
    tue_table_embed.add_field(name='Time',value=(daytuelist[0].get("time")),inline=True)
    tue_table_embed.add_field(name='Link',value=(daytuelist[0].get("link")),inline=True)
    for i in range(9):
        j = i+1
        sum =[]
        subject = (daytuelist[j].get("subject"))
        time =(daytuelist[j].get("time"))
        link = (daytuelist[j].get("link"))
        sum.append(subject)
        sum.append(time)
        sum.append(link)
        mix = " | ".join(sum)
        tue_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)

    #wed
    wed_table_embed = discord.Embed(
        title= "TimeTable of "+ "wedsday",
        description="Date & Time : "+now.strftime("%c"),
        color= Cwednesday
    )
    wed_table_embed.add_field(name='Subject',value=(daywedlist[0].get("subject")),inline=True)
    wed_table_embed.add_field(name='Time',value=(daywedlist[0].get("time")),inline=True)
    wed_table_embed.add_field(name='Link',value=(daywedlist[0].get("link")),inline=True)
    for i in range(9):
        j = i+1
        sum =[]
        subject = (daywedlist[j].get("subject"))
        time =(daywedlist[j].get("time"))
        link = (daywedlist[j].get("link"))
        sum.append(subject)
        sum.append(time)
        sum.append(link)
        mix = " | ".join(sum)
        wed_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)

    #thu
    thu_table_embed = discord.Embed(
        title= "TimeTable of "+ "thusday",
        description="Date & Time : "+now.strftime("%c"),
        color= Cthursday
    )
    thu_table_embed.add_field(name='Subject',value=(daythulist[0].get("subject")),inline=True)
    thu_table_embed.add_field(name='Time',value=(daythulist[0].get("time")),inline=True)
    thu_table_embed.add_field(name='Link',value=(daythulist[0].get("link")),inline=True)
    for i in range(9):
        j = i+1
        sum =[]
        subject = (daythulist[j].get("subject"))
        time =(daythulist[j].get("time"))
        link = (daythulist[j].get("link"))
        sum.append(subject)
        sum.append(time)
        sum.append(link)
        mix = " | ".join(sum)
        thu_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)
    
    #fri
    fri_table_embed = discord.Embed(
        title= "TimeTable of "+ "frisday",
        description="Date & Time : "+now.strftime("%c"),
        color= Cfriday
    )
    fri_table_embed.add_field(name='Subject',value=(dayfrilist[0].get("subject")),inline=True)
    fri_table_embed.add_field(name='Time',value=(dayfrilist[0].get("time")),inline=True)
    fri_table_embed.add_field(name='Link',value=(dayfrilist[0].get("link")),inline=True)
    for i in range(9):
        j = i+1
        sum =[]
        subject = (dayfrilist[j].get("subject"))
        time =(dayfrilist[j].get("time"))
        link = (dayfrilist[j].get("link"))
        sum.append(subject)
        sum.append(time)
        sum.append(link)
        mix = " | ".join(sum)
        fri_table_embed.add_field(name='--------------------------------------------------',value=mix,inline=False)
    
    #help
    help_embed = discord.Embed(
        title= "HELP",
        description="Date & Time : "+now.strftime("%c"),
        color= discord.Colour.teal()
    )
    help_embed.add_field(name='Study now',value=".now",inline=False)
    help_embed.add_field(name='Table of Today',value=".today",inline=False)
    help_embed.add_field(name='Table of Monday',value=".mon",inline=False)
    help_embed.add_field(name='Table of Tuesday',value=".tue",inline=False)
    help_embed.add_field(name='Table of Wednesday',value=".wed",inline=False)
    help_embed.add_field(name='Table of Thursday',value=".thu",inline=False)
    help_embed.add_field(name='Table of Friday',value=".fri",inline=False)

    #kuy
    kuy_embed = discord.Embed(
        title= "Kuy rai!!!!",
        description="Date & Time : "+now.strftime("%c"),
        color= 0xFF0000
    )
    kuy_embed.set_image(url='https://c.tenor.com/ojGSDL9QIQAAAAAC/mr-bean-fuck-you.gif')

    #commands
    msg = message.content
    if msg == '.now':
        await message.channel.send(embed=now_table_embed)
    if msg == '.today':
        await message.channel.send(embed=today_table_embed)
    if msg == '.mon':
        await message.channel.send(embed=mon_table_embed)
    if msg == '.tue':
        await message.channel.send(embed=tue_table_embed)
    if msg == '.wed':
        await message.channel.send(embed=wed_table_embed)
    if msg == '.thu':
        await message.channel.send(embed=thu_table_embed)
    if msg == '.fri':
        await message.channel.send(embed=fri_table_embed)
    if msg == '.h':
        await message.channel.send(embed=help_embed)
    if msg == '.kuy':
        await message.channel.send(embed=kuy_embed)

client.run(TOKEN)
