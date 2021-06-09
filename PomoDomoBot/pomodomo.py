import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import discord
from discord.ext import commands
import time
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

TOKEN = 'ODIyNTc2ODE0ODIwMDMyNTEy.YFUSWw.mlecg4MLqy_RNpJfTtXi5qLPelQ'
BOT_PREFIX = '['

bot = commands.Bot(command_prefix=BOT_PREFIX)

client = commands.Bot(command_prefix = '[')

intents = discord.Intents.default()

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")


#JOINS VOICE CALL

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

#LEAVES VOICE CALL

@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


#PLAYS MUSIC

@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

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


#POMODORO AUDIO BOT

@bot.command(pass_context=True)


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

@bot.command(name='pmdr_start')
async def start_pomodoro_timer(ctx, work_time: int, break_time: int):
    """ Start pomodoro timer
    Action:
        Start break_time timer after work_time timer
    Args:
        work_time : work timer (minute)
        break_time : break timer after work_time (minute)
    """

    if len(sched.get_jobs()) > 0:
        await ctx.channel.send(
            f"```css\n[⚠️Pomodoro timer already working!]\n - stop command : !pmdr_stop```")
        return

    async def break_schedule(work_time, break_time):
        print('Enter break schedule')
        await ctx.channel.send(
            f"{ctx.author.mention}```css\n[🔥Break time end!] Let's work :)```")
        work_expire_time = get_expire_time(work_time)
        sched.add_job(work_schedule, 'date', run_date=work_expire_time, args=[
                      work_time, break_time], misfire_grace_time=300)
        pass

    async def work_schedule(work_time, break_time):
        print('Enter work schedule')
        await ctx.channel.send(
            f"{ctx.author.mention}```css\n[🏁Work time end!] Let's break :)```")
        break_expire_time = get_expire_time(break_time)
        sched.add_job(break_schedule, 'date', run_date=break_expire_time,
                      args=[work_time, break_time], misfire_grace_time=300)
        pass

    work_expire_time = get_expire_time(work_time)
    sched.add_job(work_schedule, 'date', run_date=work_expire_time,
                  args=[work_time, break_time], misfire_grace_time=300)

    await ctx.channel.send(
        f"```css\n[Work {work_time}min, Break {break_time}min] Pomodoro Timer START.\n - stop command : !pmdr_stop```")


@bot.command(name='pmdr_stop')
async def stop_pomodoro_timer(ctx):
    """ Stop pomodoro timer
    Action:
        Stop pomodoro timer
    """
    sched.remove_all_jobs()
    await ctx.channel.send(
        f"```css\nPomodoro Timer STOP.\n - start command : !pmdr_start [work_min] [break_min]```")


bot.run(TOKEN)

bot.run(TOKEN)