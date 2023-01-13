import os, random
import discord
from dotenv import load_dotenv
import yfinance as yf
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.message_content = True

# bot = discord.Client(intents=intents)
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

        tickerData = yf.Ticker(symbol)
        todayData = tickerData.history(period='1d')
        last_close = str(round(todayData['Close'][0], 2)) 
        # stock = yf.Ticker(symbol).info
        await ctx.send(f'{symbol} last close price : ${last_close}')


bot.run(TOKEN)