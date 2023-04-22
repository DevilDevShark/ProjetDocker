import discord
import requests
from discord.ext import commands

TOKEN = 'MTA5OTIzMDI1MTkyMzU0NjIwMg.GYceqz.1isHjZp1m97_J_-ipsvCBQ9VvGxq9Dy150j0zc'

API_URL = 'http://localhost:5001'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='create', help='Create a new petition')
async def create(ctx, title: str, content: str, duration: str = '1h'):
    data = {'title': title, 'content': content, 'duration': duration}
    response = requests.post(f'{API_URL}/petitions', json=data)

    if response.status_code == 201:
        await ctx.send(f'Petition "{title}" has been created!')
    else:
        await ctx.send('Failed to create the petition.')


@bot.command(name='vote', help='Vote for a petition')
async def vote(ctx, petition_id: int, vote: str):
    data = {'petition_id': petition_id, 'user_id': ctx.author.id, 'vote': vote}
    response = requests.post(f'{API_URL}/votes', json=data)

    if response.status_code == 201:
        await ctx.send(f'Vote for petition #{petition_id} has been recorded!')
    else:
        await ctx.send('Failed to record your vote.')


@bot.command(name='close', help='Close a petition')
async def close(ctx, petition_id: int):
    response = requests.put(f'{API_URL}/petitions/{petition_id}/close')

    if response.status_code == 200:
        await ctx.send(f'Petition #{petition_id} has been closed!')
    else:
        await ctx.send('Failed to close the petition.')

bot.run(TOKEN)
