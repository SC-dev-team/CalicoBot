"""a core of CalicoBot
"""
import os
import json  # due to load user karma

import discord
from discord.ext import commands
from discord import app_commands

import embeds
import command
import event

bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    "mod!"), intents=discord.Intents.all(), activity=discord.Game(name="mod!help"))
bot.remove_command("help")
Token = os.environ['DISCORD_BOT_TOKEN']  # Load Bot Token


def load_user_karma(file_path="./user_karma_list.json"):
    """load user karma form path to json file

    Args:
        file_path (str, optional): Please set to path of json file. 
        Defaults to "./user_karma_list.json".

    Returns:
        dict: result ob json.load
    """
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            # load = fileobj to dict #loads = string to dict
            _user_karma_list = json.load(file)
        return _user_karma_list
    return {}


def save_user_karma(content, file_path="./user_karma_list.json"):
    """save our user karma

    Args:
        content (dict): users' karma list
        file_path (str, optional): Please set to path of json file. 
        Defaults to "./user_karma_list.json".
    """
    with open(file_path, "w+", encoding="utf-8") as file:
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
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server")
    )
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")
    except discord.app_commands.TranslationError:
        print("TranslationError. Please restart later...")
    except discord.app_commands.MissingApplicationID:
        print("Missing ApplicationID. Exiting...")
        raise
    except discord.app_commands.CommandSyncFailure:
        print("Some commands worng . Exiting...")
        raise
    except discord.Forbidden:
        print(
            "Don't have permission in some server. Couldn't sync command in some server...")
    except discord.HTTPException:
        print("HTTPException. Please restart later...")

# help command


@bot.command(name="help")
async def help_command(ctx):
    """When user use mod! help,Invoke this
    """
    help_embed = embeds.gen_help(ctx.guild.name)  # set footer
    await ctx.send(embed=help_embed)


@bot.tree.command(name="bothelp", description="このbotのヘルプを表示します")
async def help_tree_command(interaction: discord.Interaction):
    """When user use /bothelp,Invoke this
    """
    help_embed = embeds.gen_help(interaction.guild.name)  # set footer
    await interaction.response.send_message(embed=help_embed)

# @bot.command


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member,
                      reason: str = "無し", delete_message_days: int = 0):
    """When user use mod! ban,Invoke this
    """
    await member.ban(reason=reason, delete_message_days=delete_message_days)
    await ctx.send(embed=embeds.gen_managelog(
        member.display_name,
        ctx.author.mention,
        "BAN",
        reason,
        ctx.guild.name
    ))


@bot.command(name="gban")
@commands.has_permissions(ban_members=True)
async def gban_command(ctx, member: discord.Member,
                       reason: str = "無し", delete_message_days: int = 0):
    """When user use mod! gban,Invoke this
    """
    if not member.id in user_karma_list:
        user_karma_list[member.id] = 0
    user_karma_list[member.id] -= 1

    await member.ban(reason=reason, delete_message_days=delete_message_days)
    await ctx.send(embed=embeds.gen_managelog(member.display_name,
                                              ctx.author.mention,
                                              "グローバルBAN", reason, ctx.guild.name))


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, reason: str = "無し"):
    """When user use mod! kick,Invoke this
    """
    await member.kick(reason=reason)
    await ctx.send(embed=embeds.gen_managelog(
        member.display_name,
        ctx.author.mention,
        "kick",
        reason,
        ctx.guild.name)
    )


@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_command(ctx, member: discord.User, reason: str = "無し"):
    """When user use mod! unban,Invoke this
    """
    guild = discord.Guild

    await guild.unban(self=ctx.guild, user=member, reason=reason)
    await ctx.send(embed=embeds.gen_managelog(member.display_name,
                                              ctx.author.mention,
                                              "unBAN",
                                              reason,
                                              ctx.guild.name))

event.BotEvents()
bot.tree.add_command(command.ModCommands("mod"))
bot.tree.add_command(command.MemberCommands("member"))
try:
    bot.run(Token)
finally:
    save_user_karma(user_karma_list)
