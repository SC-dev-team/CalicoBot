import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

bot = commands.Bot(command_prefix=commands.when_mentioned_or("mod!"),intents=discord.Intents.all(),activity=discord.Game(name="mod!help"))
bot.remove_command("help")
Token = "MTE0NDA4NDA1MDg0NDMxOTgwNA.GC7XB_.nbcgqM26gGtk8NgJvK8oQt8q3mc47GnLwpgCrI"

#on ready
@bot.event
async def on_ready():
    print("起動しました")
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")
    except Exception as e:
        print(e)

#help command
@bot.command(name="help")
async def help_command(ctx):
    helpEmbed = discord.Embed(title="CalicoBot Help",color=discord.Color.green(),timestamp=datetime.now())
    helpEmbed.add_field(name="",value="prefix `mod!`",inline=False)
    helpEmbed.add_field(name="",value="`help` 今表示されてるやつを表示します",inline=False)
    helpEmbed.add_field(name="",value="`ban` メンバーをBANします",inline=False)
    helpEmbed.add_field(name="",value="`kick` メンバーをキックします",inline=False)
    helpEmbed.add_field(name="",value="`unban` メンバーをunBANします",inline=False)
    helpEmbed.add_field(name="",value="prefix `/`",inline=False)
    helpEmbed.add_field(name="",value="`member ban` メンバーをBANします",inline=False)
    helpEmbed.add_field(name="",value="`member kick` メンバーをキックします",inline=False)
    helpEmbed.add_field(name="",value="`member unban` メンバーをunBANします",inline=False)
    helpEmbed.set_footer(text=ctx.guild.name)

    await ctx.send(embed=helpEmbed)

@bot.tree.command(name="bothelp",description="このbotのヘルプを表示します")
async def help_tree_command(interaction: discord.Interaction):
    helpEmbed = discord.Embed(title="CalicoBot Help",color=discord.Color.green(),timestamp=datetime.now())
    helpEmbed.add_field(name="",value="prefix `mod!`",inline=False)
    helpEmbed.add_field(name="",value="`help` 今表示されてるやつを表示します",inline=False)
    helpEmbed.add_field(name="",value="`ban` メンバーをBANします",inline=False)
    helpEmbed.add_field(name="",value="`kick` メンバーをキックします",inline=False)
    helpEmbed.add_field(name="",value="`unban` メンバーをunBANします",inline=False)
    helpEmbed.add_field(name="",value="prefix `/`",inline=False)
    helpEmbed.add_field(name="",value="`help` 今表示されてるやつを表示します",inline=False)
    helpEmbed.add_field(name="",value="`member ban` メンバーをBANします",inline=False)
    helpEmbed.add_field(name="",value="`member kick` メンバーをキックします",inline=False)
    helpEmbed.add_field(name="",value="`member unban` メンバーをunBANします",inline=False)
    helpEmbed.set_footer(text=interaction.guild.name)

    await interaction.response.send_message(embed=helpEmbed)

#@bot.command
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, reason: str = "無し", deleteMessageDays: int = 0):
    banEmbed = discord.Embed(title=f"{member.display_name}をBANしました",color=discord.Color.red(),timestamp=datetime.now())
    banEmbed.add_field(name="担当者",value=ctx.author.mention)
    banEmbed.add_field(name="理由",value=f"`{reason}`")
    banEmbed.set_footer(text=ctx.guild.name)

    await member.ban(reason=reason,delete_message_days=deleteMessageDays)
    await ctx.send(embed=banEmbed)

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, reason: str = "無し"):
    kickEmbed = discord.Embed(title=f"{member.display_name}をkickしました",color=discord.Color.red(),timestamp=datetime.now())
    kickEmbed.add_field(name="担当者",value=ctx.author.mention)
    kickEmbed.add_field(name="理由",value=f"`{reason}`")
    kickEmbed.set_footer(text=ctx.guild.name)

    await member.kick(reason=reason)
    await ctx.send(embed=kickEmbed)

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_command(ctx, member: discord.User, reason: str = "無し"):
    guild = discord.Guild
    unbanEmbed = discord.Embed(title=f"{member.display_name}をunBANしました",color=discord.Color.green(),timestamp=datetime.now())
    unbanEmbed.add_field(name="担当者",value=ctx.author.mention)
    unbanEmbed.add_field(name="理由",value=f"`{reason}`")
    unbanEmbed.set_footer(text=ctx.guild.name)

    await guild.unban(self=ctx.guild,user=member,reason=reason)
    await ctx.send(embed=unbanEmbed)

#@bot.tree.command
class removeMember(app_commands.Group):
    def __init__(self, name: str):
        super().__init__(name=name)
    @app_commands.command(description="指定したメンバーをBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(days="BANしたユーザーのメッセージ削除の期間")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "無し", days: int = 0):
        banEmbed = discord.Embed(title=f"{member.display_name}をBANしました",color=discord.Color.red(),timestamp=datetime.now())
        banEmbed.add_field(name="担当者",value=interaction.user.mention)
        banEmbed.add_field(name="理由",value=f"`{reason}`")
        banEmbed.set_footer(text=interaction.guild.name)

        await member.ban(reason=reason,delete_message_days=days)
        await interaction.response.send_message(embed=banEmbed)

    @app_commands.command(description="指定したメンバーをKICKします")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "無し"):
        kickEmbed = discord.Embed(title=f"{member.display_name}をkickしました",color=discord.Color.red(),timestamp=datetime.now())
        kickEmbed.add_field(name="担当者",value=interaction.user.mention)
        kickEmbed.add_field(name="理由",value=f"`{reason}`")
        kickEmbed.set_footer(text=interaction.guild.name)

        await member.kick(reason=reason)
        await interaction.response.send_message(embed=kickEmbed)

    @app_commands.command(description="指定したメンバーをunBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: discord.User, reason: str = "無し"):
        guild = interaction.guild
        unbanEmbed = discord.Embed(title=f"{member.display_name}をunBANしました",color=discord.Color.green(),timestamp=datetime.now())
        unbanEmbed.add_field(name="担当者",value=interaction.user.mention)
        unbanEmbed.add_field(name="理由",value=f"`{reason}`")
        unbanEmbed.set_footer(text=interaction.guild.name)

        await guild.unban(user=member,reason=reason)
        await interaction.response.send_message(embed=unbanEmbed)

#@bot.event
@bot.event
async def on_guild_join(guild: discord.Guild):
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))

@bot.event
async def on_guild_remove(guidl: discord.Guild):
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))

bot.tree.add_command(removeMember("member"))
bot.run(Token)