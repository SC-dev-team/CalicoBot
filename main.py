"""a core of CalicoBot
"""
import os
import json  # due to load user karma

import discord
from discord.ext import commands
from discord import app_commands

import embeds

bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    "mod!"), intents=discord.Intents.all(), activity=discord.Game(name="mod!help"))
bot.remove_command("help")
Token = os.environ['DISCORD_BOT_TOKEN']  # Load Bot Token


def load_user_karma(file_path="./user_karma_list.json"):
    """load user karma form path to json file

    Args:
        file_path (str, optional): Please set to path of json file. Defaults to "./user_karma_list.json".

    Returns:
        dict: result ob json.load
    """    
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            # load = fileobj to dict #loads = string to dict
            user_karma_list = json.load(file)
        return user_karma_list
    else:
        return dict()


def save_user_karma(content, file_path="./user_karma_list.json"):
    """save our user karma

    Args:
        content (dict): users' karma list
        file_path (str, optional): Please set to path of json file. Defaults to "./user_karma_list.json".
    """    
    with open(file_path, "w+") as file:
        # dump = dict to fileobj #loads = dict to string
        json.dump(content, file)


# load user karma
user_karma_list = load_user_karma()

# on ready
@bot.event
async def on_ready():
    """Call when discord bot's status is ready
    """    
    print("起動しました")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")
    except Exception as e:
        print(e)

# help command


@bot.command(name="help")
async def help_command(ctx):    
    helpEmbed = embeds.gen_help(ctx.guild.name)  # set footer
    await ctx.send(embed=helpEmbed)


@bot.tree.command(name="bothelp", description="このbotのヘルプを表示します")
async def help_tree_command(interaction: discord.Interaction):
    helpEmbed = embeds.gen_help(interaction.guild.name)  # set footer
    await interaction.response.send_message(embed=helpEmbed)

# @bot.command


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, reason: str = "無し", deleteMessageDays: int = 0):
    await member.ban(reason=reason, delete_message_days=deleteMessageDays)
    await ctx.send(embed=embeds.gen_managelog(member.display_name, ctx.author.mention, "BAN", reason, ctx.guild.name))


@bot.command(name="gban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, reason: str = "無し", deleteMessageDays: int = 0):
    if not member.id in user_karma_list:
        user_karma_list[member.id] = 0
    user_karma_list[member.id] -= 1

    await member.ban(reason=reason, delete_message_days=deleteMessageDays)
    await ctx.send(embed=embeds.gen_managelog(member.display_name, ctx.author.mention, "グローバルBAN", reason, ctx.guild.name))


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, reason: str = "無し"):
    await member.kick(reason=reason)
    await ctx.send(embed=embeds.gen_managelog(member.display_name, ctx.author.mention, "kick", reason, ctx.guild.name))


@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_command(ctx, member: discord.User, reason: str = "無し"):
    guild = discord.Guild

    await guild.unban(self=ctx.guild, user=member, reason=reason)
    await ctx.send(embed=embeds.gen_managelog(member.display_name, ctx.author.mention, "unBAN", reason, ctx.guild.name))


# @bot.tree.command
class manageMember(app_commands.Group):
    def __init__(self, name: str):
        super().__init__(name=name)

    @app_commands.command(description="指定したメンバーをBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(days="BANしたユーザーのメッセージ削除の期間")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "無し", days: int = 0):
        await member.ban(reason=reason, delete_message_days=days)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name, interaction.user.mention, "BAN", reason, interaction.guild.name))

    @app_commands.command(description="指定したメンバーをグローバルBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(days="BANしたユーザーのメッセージ削除の期間")
    async def gban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "無し", days: int = 0):
        if not member.id in user_karma_list:
            user_karma_list[member.id] = 0
        user_karma_list[member.id] -= 1

        await member.ban(reason=reason, delete_message_days=days)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name, interaction.user.mention, "グローバルBAN", reason, interaction.guild.name))

    @app_commands.command(description="指定したメンバーをKICKします")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "無し"):
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name, interaction.user.mention, "kick", reason, interaction.guild.name))

    @app_commands.command(description="指定したメンバーをunBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: discord.User, reason: str = "無し"):
        guild = interaction.guild

        await guild.unban(user=member, reason=reason)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name, interaction.user.mention, "unBAN", reason, interaction.guild.name))


# @bot.event
@bot.event
async def on_guild_join(guild: discord.Guild):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))


@bot.event
async def on_guild_remove(guidl: discord.Guild):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))

bot.tree.add_command(manageMember("member"))
try:
    bot.run(Token)
finally:
    save_user_karma(user_karma_list)
