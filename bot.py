import os, random
import discord
from dotenv import load_dotenv
import yfinance as yf
from discord.ext import commands
import sqlite3

# load secrets
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# init
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print(f'{bot.user} has connected to Discord!')

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the OG Pirate Chat!'
    )

@bot.command(name="ping")
async def some_crazy_function_name(ctx):
	await ctx.channel.send("pong")

@bot.command(name='ticker', help='Lookup Ticker info')
async def ticker(ctx, *symbols):
    for symbol in symbols:

        try:
            tickerData = yf.Ticker(symbol)
            todayData = tickerData.history(period='1d')
            last_close = str(round(todayData['Close'][0], 2)) 
            await ctx.send(f'{symbol} last close price : ${last_close}')
        except Exception as e:
            await ctx.send('try a real ticker dumbass')

@bot.command(name="timer")
async def timer(ctx, timeInput):
    try:
        try:
            time = int(timeInput)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
        if time > 86400:
            await ctx.send("I can\'t do timers over a day long")
            return
        if time <= 0:
            await ctx.send("Timers don\'t go into negatives :/")
            return
        if time >= 3600:
            message = await ctx.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
        elif time >= 60:
            message = await ctx.send(f"Timer: {time//60} minutes {time%60} seconds")
        elif time < 60:
            message = await ctx.send(f"Timer: {time} seconds")
        while True:
            try:
                await time.sleep(5)
                time -= 5
                if time >= 3600:
                    await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                elif time >= 60:
                    await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                elif time < 60:
                    await message.edit(content=f"Timer: {time} seconds")
                if time <= 0:
                    await message.edit(content="Ended!")
                    await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
                    break
            except:
                break
    except:
        await ctx.send('enter time in seconds')


bot.run(TOKEN)