"""Embeds
Create our embeds
"""
from datetime import datetime
import discord

def gen_help(name):
    """Genereate help embed

    Returns:
        HelpEmbed: insert your response
    """    
    HelpEmbed = discord.Embed(
        title="CalicoBot Help", color=discord.Color.green(), timestamp=datetime.now())
    HelpEmbed.add_field(name="", value="prefix `mod!`", inline=False)
    HelpEmbed.add_field(name="", value="`help` 今表示されてるやつを表示します", inline=False)
    HelpEmbed.add_field(name="", value="`ban` メンバーをBANします", inline=False)
    HelpEmbed.add_field(name="", value="`gban` メンバーをグローバルBANします", inline=False)
    HelpEmbed.add_field(name="", value="`kick` メンバーをキックします", inline=False)
    HelpEmbed.add_field(name="", value="`unban` メンバーをunBANします", inline=False)
    HelpEmbed.add_field(name="", value="prefix `/`", inline=False)
    HelpEmbed.add_field(
        name="", value="`member ban` メンバーをBANします", inline=False)
    HelpEmbed.add_field(
        name="", value="`member gban` メンバーをグローバルBANします", inline=False)
    HelpEmbed.add_field(
        name="", value="`member kick` メンバーをキックします", inline=False)
    HelpEmbed.add_field(
        name="", value="`member unban` メンバーをunBANします", inline=False)
    HelpEmbed.set_footer(name)

    return HelpEmbed


def gen_managelog(target, executer, method, reason, name):
    """Generate log embed

    Returns:
        LogEmbed: insert your response
    """
    LogEmbed = discord.Embed(
        title=f"{target}を{method}しました", color=discord.Color.red(), timestamp=datetime.now())
    LogEmbed.add_field(name="担当者", value=executer)
    LogEmbed.add_field(name="理由", value=f"`{reason}`")
    LogEmbed.set_footer(text=name)

    return LogEmbed
