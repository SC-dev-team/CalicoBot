import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

bot = commands.Bot(command_prefix=commands.when_mentioned_or("mod!"),intents=discord.Intents.all(),activity=discord.Game(name="mod!help"))
bot.remove_command("help")
Token = "MTE0NDA4NDA1MDg0NDMxOTgwNA.GC7XB_.nbcgqM26gGtk8NgJvK8oQt8q3mc47GnLwpgCrI"

@bot.event
async def on_ready():
    print("起動しました")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")
    except Exception as e:
        print(e)

@bot.command(name="help")
async def help_command(ctx):
    helpEmbed = discord.Embed(title="CalicoBot Help",color=discord.Color.green(),timestamp=datetime.now())
    helpEmbed.add_field(name="",value="`help` 今表示されてるやつを表示します",inline=False)
    helpEmbed.add_field(name="",value="`ban` メンバーをBANします",inline=False)
    helpEmbed.add_field(name="",value="`kick` メンバーをキックします",inline=False)
    helpEmbed.set_footer(text=ctx.guild.name)

    await ctx.send(embed=helpEmbed)

@bot.command(name="ban")
async def ban_command(ctx, member: discord.Member, reason: str, deleteMessageDays: int = 0):
    banEmbed = discord.Embed(title=f"{member.display_name}をBANしました",color=discord.Color.red(),timestamp=datetime.now())
    banEmbed.add_field(name="担当者",value=member.banner)
    banEmbed.add_field(name="理由",value=f"`{reason}`")
    banEmbed.set_footer(text=ctx.guild.name)

    await member.ban(reason=reason,delete_message_days=deleteMessageDays)
    await ctx.send(embed=banEmbed)

@bot.command(name="kick")
async def kick_command(ctx, member: discord.Member, reason: str):
    kickEmbed = discord.Embed(title=f"{member.display_name}をkickしました",color=discord.Color.red(),timestamp=datetime.now())
    kickEmbed.add_field(name="担当者",value=f"`{ctx.author.name}`")
    kickEmbed.add_field(name="理由",value=f"`{reason}`")
    kickEmbed.set_footer(text=ctx.guild.name)

    await member.kick(reason=reason)
    await ctx.send(embed=kickEmbed)

bot.run(Token)