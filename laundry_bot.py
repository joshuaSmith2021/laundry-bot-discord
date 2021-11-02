import json
import re

import requests

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

COLORS = {
    'green': 0x28a745,
    'blue' : 0x007bff,
    'red'  : 0xdc3545
}

@bot.command()
async def laundry(ctx):
    req = requests.post('http://127.0.0.1:5000/raw_status')
    status = req.json()

    machines = status['machines']
    messages = status['messages']

    washers = [x for x in machines if x[0] == 'Washer']
    dryers = [x for x in machines if x[0] == 'Dryer']

    washer_avail = any([re.match('^\d+.*$', x[2]) for x in washers])
    dryer_avail = any([re.match('^\d+.*$', x[2]) for x in dryers])
    both_booleans = [washer_avail, dryer_avail]

    current_color = 0xdedede
    if all(both_booleans):
        current_color = COLORS['green']
    elif any(both_booleans):
        current_color = COLORS['blue']
    else:
        current_color = COLORS['red']

    embed=discord.Embed(title='tšɨłkukunɨtš laundry', color=current_color)

    for msg, mch in zip(messages, [washers, dryers]):
        mch_msg = '\n'.join(map(lambda x: f'{x[0]} {x[1]}: {x[2]}', mch))
        embed.add_field(name=msg, value=mch_msg, inline=True)

    await ctx.channel.send(embed=embed)


@bot.event
async def on_ready():
    print('Bot running...')
    activity = discord.Activity(name='!laundry', type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)


with open('credentials.json') as f:
    credentials = json.loads(f.read())
    DISCORD_TOKEN = credentials['discordToken']


bot.run(DISCORD_TOKEN)
