import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import discord
from discord.ext import commands
import asyncio
import time
import random
import json
from discord import FFmpegPCMAudio
import youtube_dl
import os
import asyncio
import functools
import itertools
import math
import random
import discord
import youtube_dl
from async_timeout import timeout
from discord.utils import get

TOKEN = 'ODIyNTc2ODE0ODIwMDMyNTEy.YFUSWw.mlecg4MLqy_RNpJfTtXi5qLPelQ'
BOT_PREFIX = '['

bot = commands.Bot(command_prefix=BOT_PREFIX)

client = commands.Bot(command_prefix = '[')

intents = discord.Intents.default()

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")


#JOINS VOICE CALL AND PLAYS MUSIC

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

#POMODORO TEXT BOT

@bot.command(pass_context=True)
async def timer(ctx, *args):
    smallBreaks = 1
    workTime = 25 * 60
    smallBreakTime = 5 * 60 
    longBreakTime = 30 * 60
    if isinstance(int(args[0]), int) and isinstance(int(args[1]), int) and isinstance(int(args[2]), int):
        workTime = int(args[0]) * 60
        smallBreakTime = int(args[1]) * 60
        longBreakTime = int(args[2]) * 60
        while True:
            t = time.time()
            await ctx.send(f"{smallBreaks}/4 work cycles in progress. Next break at {time.strftime('%I:%M:%S %p', time.localtime(t + workTime))}.")
            if smallBreaks != 4:
                smallBreaks += 1
                time.sleep(workTime)
                await ctx.send(f"Small break! Start working at {time.strftime('%I:%M:%S %p', time.localtime(t + workTime + smallBreakTime))}.")
                time.sleep(smallBreakTime)
            else:
                smallBreaks = 0
                time.sleep(workTime)   
                await ctx.send(f"Long break! Start working at {time.strftime('%I:%M:%S %p', time.localtime(t + workTime + longBreakTime))}.")
                time.sleep(longBreakTime)
    else:
        await ctx.send("Arguments not given. Using default parameters.")

bot.run(TOKEN)