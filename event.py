import discord
import datetime
from discord.ext import commands
from discord import app_commands
import time
import asyncio
import difflib
import main

bot = main.bot

class BotEvents(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.Cog.listener
    async def on_message_edit(before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
        embed.add_field(name="",value=f"{before.channel.mention}でメッセージが編集されました。\n[ページ移動]({after.jump_url})",inline=False)
        embed.add_field(name="変更前",value=f"```{before.content}```",inline=False)
        embed.add_field(name="変更後",value=f"```{after.content}```",inline=False)
        embed.set_author(icon_url=before.author.avatar.url,name=before.author.global_name)
        embed.set_footer(text=before.guild.name)

        botChannel=bot.get_all_channels()
        for channel in botChannel:
            if channel.guild == before.guild:
                if isinstance(channel, discord.TextChannel):
                    webhooks=await channel.webhooks()
                    for webhook in webhooks:
                        if webhook.name == "CalicobotLog":
                            await webhook.send(embed=embed)
                            return

    @commands.Cog.listener
    async def on_member_remove(member:discord.Member):
        if member.banner == None:
            guild=member.guild
            embed=discord.Embed(title=f"`{member.global_name}`がサーバーから退出しました",color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="アカウント作成日",value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:R>")
            embed.add_field(name="アカウント参加日",value=f"<t:{int(time.mktime(member.joined_at.now().timetuple()))}:R>")
            embed.add_field(name="ID",value=f"```{member.id}```",inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=guild.name)

            botChannel=bot.get_all_channels()
            for channel in botChannel:
                if channel.guild == guild:
                    if isinstance(channel, discord.TextChannel):
                        webhooks=await channel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_message_delete(message: discord.Message):
        if message.author.bot:
            return
        embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
        embed.add_field(name="",value=f"{message.channel.mention}で{message.author.mention}のメッセージが削除されました",inline=False)
        embed.add_field(name="メッセージの内容",value=f"```{message.content}```",inline=False)
        embed.set_author(icon_url=message.author.avatar.url,name=message.author.global_name)
        embed.set_footer(text=message.guild.name)

        botChannel=bot.get_all_channels()
        for channel in botChannel:
            if channel.guild == message.guild:
                if isinstance(channel, discord.TextChannel):
                    webhooks=await channel.webhooks()
                    for webhook in webhooks:
                        if webhook.name == "CalicobotLog":
                            await webhook.send(embed=embed)
                            return

    @commands.Cog.listener
    async def on_guild_channel_create(channel: discord.abc.GuildChannel):
        guild=channel.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.channel_create):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value=f"チャンネル`{channel.name}`が作成されました",inline=False)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="タイプ",value=channel.type)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.name)
            embed.set_footer(text=channel.guild.name)

            botChannel=bot.get_all_channels()
            for eventchannel in botChannel:
                if eventchannel.guild == guild:
                    if isinstance(eventchannel, discord.TextChannel):
                        webhooks=await eventchannel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
        guild=channel.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.channel_delete):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value=f"チャンネル`{channel.name}`が削除されました",inline=False)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="タイプ",value=channel.type)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.name)
            embed.set_footer(text=channel.guild.name)

            botChannel=bot.get_all_channels()
            for eventchannel in botChannel:
                if eventchannel.guild == guild:
                    if isinstance(eventchannel, discord.TextChannel):
                        webhooks=await eventchannel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_member_ban(guild: discord.Guild, user: discord.User):
        async for action in guild.audit_logs(action=discord.AuditLogAction.ban):
            embed=discord.Embed(title=f"`{user.global_name}`がBANされました",color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="理由",value=action.reason)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user)
            embed.set_footer(text=guild.name)

            botChannel=bot.get_all_channels()
            for channel in botChannel:
                if channel.guild == guild:
                    if isinstance(channel, discord.TextChannel):
                        webhooks=await channel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_member_join(member: discord.Member):
        guild=member.guild
        embed=discord.Embed(title=f"`{member.global_name}`が参加しました",color=discord.Color.red(),timestamp=datetime.datetime.now())
        embed.add_field(name="アカウント作成日",value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:R>",inline=False)
        embed.add_field(name="ID",value=f"```{member.id}```",inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=member.guild.name)

        botChannel=bot.get_all_channels()
        for channel in botChannel:
            if channel.guild == guild:
                if isinstance(channel, discord.TextChannel):
                    webhooks=await channel.webhooks()
                    for webhook in webhooks:
                        if webhook.name == "CalicobotLog":
                            await webhook.send(embed=embed)
                            return

    @commands.Cog.listener
    async def on_member_unban(guild: discord.Guild, user: discord.User):
        async for action in guild.audit_logs(action=discord.AuditLogAction.unban):
            embed=discord.Embed(title=f"`{user.global_name}`がunBANされました",color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="ID",value=f"```{user.id}```")
            embed.set_author(icon_url=action.user.avatar.url,name=action.user)
            embed.set_footer(text=guild.name)

            botChannel=bot.get_all_channels()
            for channel in botChannel:
                if channel.guild == guild:
                    if isinstance(channel, discord.TextChannel):
                        webhooks=await channel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_guild_role_create(role: discord.Role):
        guild=role.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.role_create):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value="ロールが作成されました",inline=False)
            embed.add_field(name="名前",value=action.target.mention)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.global_name)
            embed.set_footer(text=guild.name)

            botChannel=bot.get_all_channels()
            for channel in botChannel:
                if channel.guild == guild:
                    if isinstance(channel, discord.TextChannel):
                        webhooks=await channel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_guild_role_delete(role: discord.Role):
        guild=role.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.role_delete):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value="ロールが削除されました",inline=False)
            embed.add_field(name="名前",value=role.name)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.global_name)
            embed.set_footer(text=guild.name)

            botChannel=bot.get_all_channels()
            for channel in botChannel:
                if channel.guild == guild:
                    if isinstance(channel, discord.TextChannel):
                        webhooks=await channel.webhooks()
                        for webhook in webhooks:
                            if webhook.name == "CalicobotLog":
                                await webhook.send(embed=embed)
                                return

    @commands.Cog.listener
    async def on_guild_join():
        """Generate presence when status changed
        """
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))


    @commands.Cog.listener
    async def on_guild_remove():
        """Generate presence when status changed
        """
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(name=f"mod!help | {len(bot.guilds)} server"))

#@commands.Cog.listener
#async def on_member_update(before: discord.Member, after: discord.Member):
#    guild=before.guild
#    beforeRoleList=list()
#    for beforeRole in before.roles:
#        if beforeRole.name != "@everyone":
#            beforeRoleList.append(str(beforeRole.id))#文字列でないとdiffが使えないため
#    afterRoleList=list()
#    for afterRole in after.roles:
#        if afterRole.name != "@everyone":
#            afterRoleList.append(str(afterRole.id))

#    differ = difflib.Differ()
#    diff_result_list = differ.compare(beforeRoleList, afterRoleList)

#    message = list()
#    for line in diff_result_list:
#        if line.startswith("+"):
#            message_line = f":white_check_mark:{guild.get_role(int(''.join(line[2:]))).mention}"#二文字ほどついかされるため+(スペース)|-(スペース)など
#            message.append(message_line)
#        elif line.startswith("-"):
#            message_line = f":negative_squared_cross_mark:{guild.get_role(int(''.join(line[2:]))).mention}"
#            message.append(message_line)

#        embedb=discord.Embed(title=f"`{before.global_name}`のロールが更新されました",color=discord.Color.green(),timestamp=datetime.datetime.now())
#        embedb.add_field(name="変更",value=''.join(message),inline=False)
#        embedb.set_author(icon_url=before.avatar.url,name=before.name)
#        embedb.set_footer(text=guild.name)

#        botChannel=bot.get_all_channels()
#        for channel in botChannel:
#            if channel.guild == guild:
#                if isinstance(channel, discord.TextChannel):
#                    webhooks=await channel.webhooks()
#                    for webhook in webhooks:
#                        if webhook.name == "CalicobotLog":
#                            await webhook.send(embed=embedb)
#                            return