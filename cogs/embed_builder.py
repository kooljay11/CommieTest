import discord
from discord.ext import commands


class Embed_Builder(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("embed_builder.py is ready!")

    @commands.command(aliases=["embeddy"])
    async def embedder(self, ctx, message):
        # Can also use colour=ctx.author.colour to make the message the same colour as the author
        #embed_message = discord.Embed(title="Title of embed", description="Description of embed", colour=discord.Colour.green())
        embed_message = discord.Embed(
            title="Title of embed", colour=discord.Colour.green())

        embed_message.set_author(
            name=f"Requested by {message.author.mention}", icon_url=ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        # embed_message.set_image(url=ctx.guild.icon)
        embed_message.add_field(
            name="Field name", value="Field value", inline=True)
        embed_message.set_footer(
            text="This is the footer", icon_url=ctx.author.avatar)

        await ctx.send(embed=embed_message)


async def setup(client):
    await client.add_cog(Embed_Builder(client))
