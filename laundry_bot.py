import json

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
    req = requests.post('https://a105-207-62-170-220.ngrok.io/fulfillment')
    status = req.json()

    message = status['prompt']['firstSimple']['speech']
    both_status = [x.replace('.', '') for x in message.split('. ')]
    laundry_status, dryer_status = both_status

    current_color = 0xdedede

    both_booleans = [len(x.split()) == 5 for x in both_status]
    if all(both_booleans):
        current_color = COLORS['green']
    elif any(both_booleans):
        current_color = COLORS['blue']
    else:
        current_color = COLORS['red']

    embed = discord.Embed(title="tšɨłkukunɨtš laundry", color=current_color)

    await ctx.channel.send(status['prompt']['firstSimple']['speech'])


with open('credentials.json') as f:
    credentials = json.loads(f.read())
    DISCORD_TOKEN = credentials['discordToken']


bot.run(DISCORD_TOKEN)
