import discord
from discord.ext import commands
import random


class Eightball(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("eightball.py is ready!")

    @commands.command(aliases=["8bail", "eightballing"])
    async def eightball(self, ctx, *, question):
        print("!eightball is activated")
        with open("../eightball_list.txt", "r") as f:
            randomresponses = f.readlines()
            response = random.choice(randomresponses)

        await ctx.send(response)
        print("!eightball is done")


async def setup(client):
    await client.add_cog(Eightball(client))
