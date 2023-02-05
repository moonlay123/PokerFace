import time
import discord
from discord.ext import commands
from function_poker import *


activity = discord.Game(name="Texas hold'em")
client = commands.Bot(intents=discord.Intents.default(), command_prefix='<@1050818228697432186> ', activity=activity)
game_going = game_begins = False
Players = []
PlayersID = []


@client.event
async def on_ready():
    print('bot connected!')


@client.event
async def print_chat(content):
    channel = client.get_channel(878299345823350794)
    await channel.send(content)


@client.event
async def print_pm(content, user):
    await user.send(content)


@client.command()
async def hello(ctx):
    if game_going:
        return
    await print_pm(f'Hello, <@!{ctx.author.id}>', ctx.author)
    await print_chat(f'Hello, <@!{ctx.author.id}>')


@client.command()
async def joingame(ctx):
    global game_begins, Players, PlayersID
    if not game_begins:
        return
    Players.append(ctx.author)
    PlayersID.append(ctx.author.id)
    await print_chat(f'<!@{ctx.author.id}, вы успешно присоеденились к игре')


@client.command()
async def startgame(ctx, *ids):
    global game_going, game_begins, Players, PlayersID
    ids = list(ids)
    if len(ids) == 0:
        await print_chat('Не указано участников игры')
        return

    ids.sort()
    Players = []
    game_going = game_begins = True
    starter = True
    deck = Deck()
    while starter:
        if len(ids) != len(Players):
            continue
        PlayersID.sort()
        for index in range(len(ids)):
            if PlayersID[index] != ids[index]:
                continue
        break
    list_players = 'Игра начинается, список игроков: '
    for i in PlayersID:
        list_players += f'<!@{i}>, '
    await print_chat(list_players)
    game_begins = False


    # players = int(input('Количество игроков: '))
    # chip = int(input('Количество фишек: '))
    # chips = [chip] * players
    # chips = game(deck, chips)
    # stop = True
    # while stop:
    #    stop = bool(input('Завершить игру? '))
    #    chips = game(deck, chips)

    Players = []
    PlayersID = []
    game_going = False



client.run(open('token.txt', 'r').readline())
