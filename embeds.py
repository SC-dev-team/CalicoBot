import discord
from datetime import datetime


def help(name):
    helpEmbed = discord.Embed(
        title="CalicoBot Help", color=discord.Color.green(), timestamp=datetime.now())
    helpEmbed.add_field(name="", value="prefix `mod!`", inline=False)
    helpEmbed.add_field(name="", value="`help` 今表示されてるやつを表示します", inline=False)
    helpEmbed.add_field(name="", value="`ban` メンバーをBANします", inline=False)
    helpEmbed.add_field(name="", value="`gban` メンバーをグローバルBANします", inline=False)
    helpEmbed.add_field(name="", value="`kick` メンバーをキックします", inline=False)
    helpEmbed.add_field(name="", value="`unban` メンバーをunBANします", inline=False)
    helpEmbed.add_field(name="", value="prefix `/`", inline=False)
    helpEmbed.add_field(
        name="", value="`member ban` メンバーをBANします", inline=False)
    helpEmbed.add_field(
        name="", value="`member gban` メンバーをグローバルBANします", inline=False)
    helpEmbed.add_field(
        name="", value="`member kick` メンバーをキックします", inline=False)
    helpEmbed.add_field(
        name="", value="`member unban` メンバーをunBANします", inline=False)
    helpEmbed.set_footer(name)

    return helpEmbed


def managelog(target, executer, method, reason, name):
    logEmbed = discord.Embed(
        title=f"{target}を{method}しました", color=discord.Color.red(), timestamp=datetime.now())
    logEmbed.add_field(name="担当者", value=executer)
    logEmbed.add_field(name="理由", value=f"`{reason}`")
    logEmbed.set_footer(text=name)

    return logEmbed
