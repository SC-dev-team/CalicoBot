"""Embeds
Create our embeds
"""
from datetime import datetime
import discord

def gen_help(name):
    """Genereate help embed

    Returns:
        help_embed: insert your response
    """
    help_embed = discord.Embed(
        title="CalicoBot Help", color=discord.Color.green(), timestamp=datetime.now())
    help_embed.add_field(name="", value="prefix `mod!`", inline=False)
    help_embed.add_field(name="", value="`help` 今表示されてるやつを表示します", inline=False)
    help_embed.add_field(name="", value="`ban` メンバーをBANします", inline=False)
    help_embed.add_field(name="", value="`gban` メンバーをグローバルBANします", inline=False)
    help_embed.add_field(name="", value="`kick` メンバーをキックします", inline=False)
    help_embed.add_field(name="", value="`unban` メンバーをunBANします", inline=False)
    help_embed.add_field(name="", value="prefix `/`", inline=False)
    help_embed.add_field(
        name="", value="`member ban` メンバーをBANします", inline=False)
    help_embed.add_field(
        name="", value="`member gban` メンバーをグローバルBANします", inline=False)
    help_embed.add_field(
        name="", value="`member kick` メンバーをキックします", inline=False)
    help_embed.add_field(
        name="", value="`member unban` メンバーをunBANします", inline=False)
    help_embed.set_footer(name)

    return help_embed


def gen_managelog(target, executer, method, reason, name):
    """Generate log embed

    Returns:
        log_embed: insert your response
    """
    log_embed = discord.Embed(
        title=f"{target}を{method}しました", color=discord.Color.red(), timestamp=datetime.now())
    log_embed.add_field(name="担当者", value=executer)
    log_embed.add_field(name="理由", value=f"`{reason}`")
    log_embed.set_footer(text=name)

    return log_embed
