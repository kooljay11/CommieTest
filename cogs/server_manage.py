import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("server_manage.py is ready!")

    @commands.command(aliases=["cleaner"])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} messeages(s) have been deleted.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def kick(self, ctx, member: discord.member, *, modreason):
        await ctx.guild.kick(member)
        conf_embed = discord.Embed(
            title="Success!", colour=discord.Colour.green())
        conf_embed.add_field(
            name="Kicked:", value=f"{member.mention} has been kicked from the server by {ctx.author.mention} for {modreason}", inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ban(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.ban(member)
        conf_embed = discord.Embed(
            title="Success!", colour=discord.Colour.green())
        conf_embed.add_field(
            name="Banned:", value=f"{member.mention} has been banned from the server by {ctx.author.mention} for {modreason}", inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(
            title="Success!", colour=discord.Colour.green())
        conf_embed.add_field(
            name="Unbanned:", value=f"<@{userId}> has been unbanned from the server by {ctx.author.mention}", inline=False)

        await ctx.send(embed=conf_embed)


async def setup(client):
    await client.add_cog(Moderation(client))
