import os, random
import discord
from dotenv import load_dotenv
import yfinance as yf
from discord.ext import commands
import datetime
import pandas as pd
import sqlite3

from table2ascii import table2ascii as t2a, PresetStyle

# load secrets
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# init
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# TODO: CREATE BOT CLASS
# class DiscordBot(commands.bot):
#     def __init__(self):
#         super().__init__(command_prefix="$")

#         @self.command(name='test')
#         async def custom(ctx):
#             print('hello world')

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

@bot.command(name="help")
async def help(ctx)

# SAMPLE COMMAND
@bot.command(name="ping")
async def some_crazy_function_name(ctx):
	await ctx.channel.send("pong")

# TODO: move to util
def clean_up_single_field(field: float, round_field: int = 2) -> float:
    return round((field[0]), round_field)

@bot.command(name='ticker', help='Lookup Ticker info')
async def ticker(ctx, *symbols):
    for symbol in symbols:

        try:
            tk = yf.Ticker(symbol)
            
            prev_close = tk.info['regularMarketPreviousClose']
            current = tk.info['regularMarketPrice']
            # o = tk['regularMarketOpen']
            # h = tk['regularMarketDayHigh']
            # l = tk['regularMarketDayLow']
            # c = tk['regularMarketClose']
            vol = tk.info['regularMarketVolume']
            todayData = tk.history(period='1d')

            o = clean_up_single_field(todayData['Open'])
            h = clean_up_single_field(todayData['High'])
            l = clean_up_single_field(todayData['Low'])
            c = clean_up_single_field(todayData['Close'])

            change = round(((current - prev_close) * 100 / prev_close), 2)

            output = t2a(
                header=["Instrument", "Current", "Open", "High", "Low", "Close", "Vol", "% Change"],
                body=[[symbol, current, o, h, l, c, vol, change]],
                first_col_heading=True
            )

            await ctx.send(f"```\n{output}\n```")
        except Exception as e:
            print(str(e))
            await ctx.send('try a real ticker dumbass')


@bot.command(name='opx', help="Options Chain")
async def opx(ctx, symbol: str, expiration_date: str = None) -> None:
    limit=2
    tk = yf.Ticker(symbol)
    exp = list(tk.options)

    if expiration_date == None:
        try:
            await ctx.send(f'Please select a exp date \n {exp}')
            return
        except:
            await ctx.send('error?')
            return

    try:
        opt = tk.option_chain(expiration_date)
        todayData = tk.history(period='1d')
        current = clean_up_single_field(todayData['Close'])

        # get closet strike to current close
        closest_strike_calls = opt.calls.iloc[(opt.calls['strike']-round(current)).abs().argsort()[:1]].index.values.astype(int)[0]
        limited_calls = opt.calls.iloc[closest_strike_calls-limit:closest_strike_calls+limit]

        closest_strike_puts = opt.puts.iloc[(opt.puts['strike']-round(current)).abs().argsort()[:1]].index.values.astype(int)[0]
        limited_puts = opt.puts.iloc[closest_strike_puts-limit:closest_strike_puts+limit]

        options = pd.concat([limited_calls, limited_puts])

        # change above back to opt if you want to add epx dat

        # opt['expirationDate'] = expiration_date
        # options = pd.concat([opt], ignore_index=True)
        
        # yfinance returns incorrect date, add 1 day for correct exp
        # options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days=1)

        # options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
        options['CALL'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)
        options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)

        # mid-point
        options['mark'] = (options['bid'] + options['ask']) / 2 
        
        # Drop unnecessary and meaningless columns
        options = options.drop(columns = ['contractSize', 'currency', 'change', 'lastTradeDate', 'lastPrice'])

        print(options.to_markdown(index=False))

        await ctx.send(f'{options.to_markdown(index=False)}')
    except Exception as e: 
        await ctx.send(f'Error: {str(e)}')
        



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
