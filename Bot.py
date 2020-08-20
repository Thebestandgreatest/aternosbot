import discord
from discord.ext import commands
import os
from Configure import launch_config
from dotenv import load_dotenv
import json
from connect_and_launch import start_server, get_status, stop_server

if not os.path.exists(os.path.relpath(".env")):
    launch_config()

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_STATUS_URI = "http://" + os.getenv("SERVER_STATUS_URI")
HEADER = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125"}

client = discord.Client()

@client.event
async def on_ready():
    print('The bot is logged in as {0.user}'.format(client))

    

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == '--launch':
        await message.channel.send("Attempting to launch server...")
        status = get_status()
        if status == "Offline":
            await message.channel.send("Launching the server.")
            await start_server

        elif status == "Online":
            await message.channel.send("The server is already Online")

        else :
            await message.channel.send("An error occured. Either the status server is not responding, or you didn't set the server name correctly.\nTrying to launch server anyway.")
            await start_server

    if message.content == '--status':
        await message.channel.send("Attempting to get server status...")
        status = get_status()
        await message.channel.send("The server is {}".format(status))

    if message.content == '--players':
        await message.channel.send("Attempting to get players...")
        try:
            players = get_number_of_players()
        except:
            await message.channel.send("There are 0 players on the server")
        else:
            await message.channel.send("There are {} players on the server".format(players))

    if message.content == '--stop':
        status = get_status()
        if status == "Offline":
            await message.channel.send("The server is already offline")
        else:
            await message.channel.send("Attempting to stop server...")
            await stop_server
            await message.channel.send("Stopping the server.")

    if message.content == '--help':
        e = discord.Embed(title="Help list", description="all commands need the prefix --")
        e.add_field(name="launch", value="launches the server", inline=False)
        e.add_field(name="status", value="gets the server status", inline=False)
        e.add_field(name="players", value="gets the cuurent players", inline=False)
        e.add_field(name="stop", value="stops the server", inline=False)
        e.add_field(name="help", value="displays this help  list", inline=False)
        await message.channel.send("", embed=e)
    

client.run(BOT_TOKEN)
