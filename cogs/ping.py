import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ping.py is ready!")

    @commands.command(aliases=["pingy", "pinger"])
    async def ping(self, ctx):
        bot_latency = round(self.client.latency * 1000)
        # Sends the message in the same channel it was sent in
        await ctx.send(f"Pong! {bot_latency} ms.")
        # await ctx.author.send("Pong!")#Sends the message to the user's dmsself.client.latency * 1000)


async def setup(client):
    await client.add_cog(Ping(client))
