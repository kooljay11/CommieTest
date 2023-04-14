# https://discord.com/api/oauth2/authorize?client_id=1058165404796723310&permissions=8&scope=bot
import os
import asyncio
import random
import math
import json
import discord
from discord.ext import commands, tasks


def get_server_prefix(client, message):
    with open("prefixes.json", "r") as file:
        prefix = json.load(file)

    return prefix[str(message.guild.id)]


client = commands.Bot(command_prefix=get_server_prefix,
                      intents=discord.Intents.all())


@tasks.loop(hours=24)
async def change_status():
    with open("./commie_bot_status.txt", "r") as file:
        randomresponses = file.readlines()
        response = random.choice(randomresponses)
    await client.change_presence(activity=discord.Game(response))


@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is connected to Discord")
    change_status.start()


# Makes a slash command called ping
@client.tree.command(name="ping", description="Shows bot latency in ms.")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {bot_latency} ms.")


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as file:
        prefix = json.load(file)

    prefix[str(guild.id)] = "!"

    with open("prefixes.json", "w") as file:
        json.dump(prefix, file, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as file:
        prefix = json.load(file)

    prefix.pop(str(guild.id))

    with open("prefixes.json", "w") as file:
        json.dump(prefix, file, indent=4)


@client.command()
@commands.has_permissions(administrator=True)
async def admincheck(ctx):
    await ctx.send("You're an Admin")


@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, *, newprefix: str):
    with open("prefixes.json", "r") as file:
        prefix = json.load(file)

    prefix[str(ctx.guild.id)] = newprefix

    with open("prefixes.json", "w") as file:
        json.dump(prefix, file, indent=4)


async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")


async def main():
    async with client:
        await load()
        with open("config.json", "r") as file:
            config = json.load(file)

        await client.start(config['token'])


asyncio.run(main())
