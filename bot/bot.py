import discord
import requests
import time
from discord.ext import commands

TOKEN = 'MTA5OTIzMDI1MTkyMzU0NjIwMg.GYceqz.1isHjZp1m97_J_-ipsvCBQ9VvGxq9Dy150j0zc'

API_URL = 'http://localhost:5001'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(check_petitions_duration())

async def check_petitions_duration():
    while True:
        response = requests.get(f'{API_URL}/petitions')
        if response.status_code == 200:
            petitions = response.json()
            for petition in petitions:
                if petition['duration'] != 'permanent' and time.time() > petition['expiration_time']:
                    requests.put(f'{API_URL}/petitions/{petition["id"]}/close')
        await asyncio.sleep(60)

def duration_in_minutes(duration_str):
    duration = int(duration_str[:-1])
    unit = duration_str[-1]

    if unit == 'h':
        return duration * 60
    elif unit == 'd':
        return duration * 60 * 24
    else:
        raise ValueError('Invalid duration unit')

@bot.command(name='create', help='Create a new petition')
@commands.has_role('admin')
async def create(ctx, title: str, content: str, duration: str = '1h'):
    try:
        duration_in_minutes = duration_in_minutes(duration)
    except ValueError as e:
        await ctx.send(str(e))
        return

    data = {'title': title, 'content': content, 'duration': duration_in_minutes}
    response = requests.post(f'{API_URL}/petitions', json=data)

    if response.status_code == 201:
        await ctx.send(f'Petition "{title}" has been created!')
    else:
        await ctx.send('Failed to create the petition.')

@bot.command(name='vote', help='Vote for a petition')
async def vote(ctx, petition_id: int, vote: str):
    if vote.lower() in ['oui', 'yes']:
        vote = 'yes'
    elif vote.lower() in ['non', 'no']:
        vote = 'no'
    else:
        await ctx.send('Invalid vote option. Please vote with "oui" or "non"')
        return
    
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

@bot.command(name='get_petition_id', help='Get the ID of a petition by its name')
async def get_petition_id(ctx, name: str):
    response = requests.get(f'{API_URL}/petitions?title={name}')
    if response.status_code == 200:
        petition = response.json()
        await ctx.send(f'The ID of petition "{name}" is {petition["id"]}')
    else:
        await ctx.send('Failed to find the petition.')

bot.run(TOKEN)