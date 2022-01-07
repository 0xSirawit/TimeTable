#Setup
import json
import datetime
import pytz
import discord
from discord import message
from discord import embeds
from discord import DMChannel
from discord.colour import Color
from discord.embeds import Embed
from keep_alive import keep_alive

client = discord.Client()
TOKEN="" #bot's token

#Main
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="⚙️.helpt"))
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #Set time
    tz_thai = pytz.timezone("Asia/Bangkok")
    now = datetime.datetime.now(tz_thai)
    today = now.strftime("%A")
    #Read json file 
    myjsonfile=open('Time.json','r')
    jsondata=myjsonfile.read()
    obj=json.loads(jsondata)
    daylist=obj[today]

    #Weekday colors
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

    #Orderfunction
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
            time =(obj[day][j].get("time"))
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

    #Commands
    msg = message.content
    if msg == '.now':
        await message.channel.send(embed=now_table_embed)
    if msg == '.next':
        await message.channel.send(embed=next_table_embed)
    if msg == '.today':
        await message.channel.send(embed=daytimetable(today, color_today))
    if msg == '.td':
        await message.channel.send(embed=daytimetable(today, color_today))
    if msg == '.mon':
        await message.channel.send(embed=daytimetable("Monday", Cmonday))
    if msg == '.tue':
        await message.channel.send(embed=daytimetable("Tuesday", Ctuesday))
    if msg == '.wed':
        await message.channel.send(embed=daytimetable("Wednesday", Cwednesday))
    if msg == '.thu':
        await message.channel.send(embed=daytimetable("Thursday", Cthursday))
    if msg == '.fri':
        await message.channel.send(embed=daytimetable("Friday", Cfriday))
    if msg == '.helpt':
        await message.channel.send(embed=help_embed)

keep_alive()
client.run(TOKEN)
