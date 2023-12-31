"""
Implementing CalicoBot events
"""
import datetime
import time

import discord
from discord.ext import commands

BOT = None
def event_init(main_bot):
    """
    A function to initialize event module
    Args:
        main_bot (discord.bot): set your bot instance to get channels
    """
    global BOT# pylint: disable=global-statement
    BOT = main_bot

class BotEvents(commands.Cog):
    """BotEventsClass
        Its function will be registered when bot will start
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """
        When user edit message,Invoke this.
        """
        if before.author.bot:
            return
        embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
        embed.add_field(name="",
                        value=f"{before.channel.mention}でメッセージが編集されました。\n[ページ移動]({after.jump_url})",
                        inline=False)
        embed.add_field(name="変更前",value=f"```{before.content}```",inline=False)
        embed.add_field(name="変更後",value=f"```{after.content}```",inline=False)
        embed.set_author(icon_url=before.author.avatar.url,name=before.author.global_name)
        embed.set_footer(text=before.guild.name)

        for channel in before.guild.text_channels:
            webhooks=await channel.webhooks()
            webhook = discord.utils.get(webhooks,name="CalicobotLog")
            # Return webhook object named CalicobotLog
            # If it can't find webhook, it will return None
            if webhook:
                await webhook.send(embed=embed)
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        """
        When user is kicked or is banned or leave from server,Invoke this.
        """
        if member.banner is None:
            guild=member.guild
            embed=discord.Embed(title=f"`{member.global_name}`がサーバーから退出しました",
                                color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="アカウント作成日",
                            value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:R>")
            embed.add_field(name="アカウント参加日",
                            value=f"<t:{int(time.mktime(member.joined_at.now().timetuple()))}:R>")
            embed.add_field(name="ID",value=f"```{member.id}```",inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=guild.name)

            for channel in guild.text_channels:
                webhooks=await channel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        When user delete message,Invoke this.
        """
        if message.author.bot:
            return
        embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
        embed.add_field(
            name="",value=f"{message.channel.mention}で{message.author.mention}のメッセージが削除されました",
            inline=False)
        embed.add_field(name="メッセージの内容",value=f"```{message.content}```",inline=False)
        embed.set_author(icon_url=message.author.avatar.url,name=message.author.global_name)
        embed.set_footer(text=message.guild.name)

        for channel in message.guild.text_channels:
            webhooks = await channel.webhooks()
            webhook = discord.utils.get(webhooks,name="CalicobotLog")
            # Return webhook object named CalicobotLog
            # If it can't find webhook, it will return None
            if webhook:
                await webhook.send(embed=embed)
                return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """
        When moderetor create channel,Invoke this.
        """
        guild=channel.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.channel_create):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value=f"チャンネル`{channel.name}`が作成されました",inline=False)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="タイプ",value=channel.type)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.name)
            embed.set_footer(text=channel.guild.name)

            for eventchannel in guild.text_channels:
                webhooks=await eventchannel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        """
        When moderetor delete channel,Invoke this.
        """
        guild=channel.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.channel_delete):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value=f"チャンネル`{channel.name}`が削除されました",inline=False)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="タイプ",value=channel.type)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.name)
            embed.set_footer(text=channel.guild.name)

            for eventchannel in guild.text_channels:
                webhooks=await eventchannel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        """
        When moderetor ban member,Invoke this.
        """
        async for action in guild.audit_logs(action=discord.AuditLogAction.ban):
            embed=discord.Embed(title=f"`{user.global_name}`がBANされました",
                                color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="理由",value=action.reason)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user)
            embed.set_footer(text=guild.name)

            for channel in guild.text_channels:
                webhooks=await channel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        When member join to the server,Invoke this.
        """
        guild=member.guild
        embed=discord.Embed(title=f"`{member.global_name}`が参加しました",
                            color=discord.Color.red(),timestamp=datetime.datetime.now())
        embed.add_field(name="アカウント作成日",
                        value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:R>",
                        inline=False)
        embed.add_field(name="ID",value=f"```{member.id}```",inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=member.guild.name)

        for channel in guild.text_channels:
            webhooks=await channel.webhooks()
            webhook = discord.utils.get(webhooks,name="CalicobotLog")
            # Return webhook object named CalicobotLog
            # If it can't find webhook, it will return None
            if webhook:
                await webhook.send(embed=embed)
                return

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        """
        When moderetor unban member,Invoke this.
        """
        async for action in guild.audit_logs(action=discord.AuditLogAction.unban):
            embed=discord.Embed(title=f"`{user.global_name}`がunBANされました",
                                color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="担当者",value=action.user.mention)
            embed.add_field(name="ID",value=f"```{user.id}```")
            embed.set_author(icon_url=action.user.avatar.url,name=action.user)
            embed.set_footer(text=guild.name)

            for channel in guild.text_channels:
                webhooks=await channel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        """
        When moderetor create role,Invoke this.
        """
        guild=role.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.role_create):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value="ロールが作成されました",inline=False)
            embed.add_field(name="名前",value=action.target.mention)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.global_name)
            embed.set_footer(text=guild.name)

            for channel in guild.text_channels:
                webhooks=await channel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """
        When moderetor delete role,Invoke this.
        """
        guild=role.guild
        async for action in guild.audit_logs(action=discord.AuditLogAction.role_delete):
            embed=discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.now())
            embed.add_field(name="",value="ロールが削除されました",inline=False)
            embed.add_field(name="名前",value=role.name)
            embed.add_field(name="担当者",value=action.user.mention)
            embed.set_author(icon_url=action.user.avatar.url,name=action.user.global_name)
            embed.set_footer(text=guild.name)

            for channel in guild.text_channels:
                webhooks = await channel.webhooks()
                webhook = discord.utils.get(webhooks,name="CalicobotLog")
                # Return webhook object named CalicobotLog
                # If it can't find webhook, it will return None
                if webhook:
                    await webhook.send(embed=embed)
                    return

    @commands.Cog.listener()
    async def on_guild_join(self):
        """Generate presence when status changed
        """
        await self.bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(
                                      name=f"mod!help | {len(BOT.guilds)} server"))


    @commands.Cog.listener()
    async def on_guild_remove(self):
        """Generate presence when status changed
        """
        await self.bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(
                                      name=f"mod!help | {len(BOT.guilds)} server"))

async def setup(bot):
    """
    Call when execution bot's reload commands or bot's status is ready
    """
    await bot.add_cog(BotEvents(bot))
