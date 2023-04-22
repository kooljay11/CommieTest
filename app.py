# https://discord.com/api/oauth2/authorize?client_id=1058165404796723310&permissions=8&scope=bot
import os
import asyncio
import random
import math
import json
import discord
from discord.ext import commands, tasks
# from discord import option
# from nextcord import SlashOption


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


class TestMenuButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Test1", style=discord.ButtonStyle.blurple)
    async def test(self, interaction: discord.Interaction, Buttton: discord.ui.Button):
        await interaction.channel.send(content="I've been clicked!")

    @discord.ui.button(label="Click me", style=discord.ButtonStyle.green)
    async def test2(self, interaction: discord.Interaction, Buttton: discord.ui.Button):
        await interaction.channel.send(content="Clicked!")

    @discord.ui.button(label="Test3", style=discord.ButtonStyle.primary)
    async def test3(self, interaction: discord.Interaction, Buttton: discord.ui.Button):
        await interaction.channel.send(content="Test 3 clicked")

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def test4(self, interaction: discord.Interaction, Buttton: discord.ui.Button):
        await interaction.channel.send(content="Exiting Menu...")


@client.tree.command(name="helpmenu")
async def buttonmenu(interaction: discord.Interaction):
    await interaction.response.send_message(content="Here's my button menu!", view=TestMenuButton())


@client.tree.command(name="dev", description="Developer only command.")
async def dev(interaction: discord.Interaction):
    print("Dev command running")
    print(f"interaction.user.id == {interaction.user.id}")

    with open("developer_list.txt", "r") as file:
        dev_list = file.readlines()

    print(f"dev_list: {dev_list}")

    # if interaction.user.id == 107886996365508608:
    if str(interaction.user.id) in dev_list:
        await interaction.response.send_message("Command ran successfully. You are a developer.")
    else:
        await interaction.response.send_message("Cannot run command, because you are not a developer.")


@client.tree.command(name="optioncommand", description="Slash command that allows for options.")
async def optioncommand(interaction: discord.Interaction, companion: str, times: int = None):
    # async def optioncommand(interaction: discord.Interaction, option1: str, option2: int = SlashOption(name="picker", choices={"30pt": 30, "50pt": 50, "80pt": 80})):
    await interaction.response.send_message(f"Went out with {companion} {times} times.")


# Makes a slash command called ping
@client.tree.command(name="ping", description="Shows bot latency in ms.")
async def ping(interaction: discord.Interaction):
    commands_channel = discord.utils.get(
        interaction.guild.channels, name="bot-testing")

    if interaction.channel.id == commands_channel.id:
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
