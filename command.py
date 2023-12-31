"""
Implementing CalicoBot commands
"""
import datetime
import time
import discord
from discord import app_commands
from discord.ext import commands

import embeds

user_karma_list=[]
def command_init(main_list):
    """A function to initialize command module
    Args:
        main_list (list): input your user karma data
    """
    global user_karma_list# pylint: disable=global-statement
    user_karma_list = main_list

class Member(commands.GroupCog):
    """MemberCommands Class

        Its function will be registered when bot will start
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="サーバーの情報を表示します")
    async def serverinfo(self, interaction: discord.Interaction):
        """
        A command to show server infomation
        """
        guild=interaction.guild
        member_list = filter(
            lambda member: member.status == discord.Status.online,
            guild.members
        )
        guild_online_member = len(list(member_list))
        rlb = " | ".join([role.mention for role in guild.roles])
        embed=discord.Embed(title=f"{guild.name} - Info",color=discord.Color.blue(),
                            timestamp=datetime.datetime.now())
        embed.add_field(name="作成日",value=f"<t:{int(guild.created_at.timestamp())}:R>")
        embed.add_field(name="サーバーID",value=f"{guild.id}")
        embed.add_field(name="所有者",value=guild.owner.mention)
        embed.add_field(name=f"メンバー数({guild.member_count})",
                        value="\n".join([f"**{str(guild_online_member)}** オンライン",
                                         f"**{guild.premium_subscription_count}** ブースター"])
                                         )
        embed.add_field(name=f"チャンネル数({len(guild.channels)})",
                        value="\n".join([f"**{len(guild.text_channels)}** テキストチャンネル",
                                    f"**{len(guild.voice_channels)}** ボイスチャンネル"])
                                    )
        embed.add_field(name=f"ロール({len(guild.roles)})",value="".join([rlb]),inline=False)
        embed.set_author(icon_url=interaction.user.avatar.url,name=interaction.user.global_name)
        embed.set_footer(text=guild.name)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="指定したユーザーの情報を表示します")
    @app_commands.describe(user="情報を表示したいユーザーを指定します")
    async def info(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        A command to show information of a specified user
        """
        guild=interaction.guild

        if user is None:
            role_list=[]
            for role in interaction.user.roles:
                if role.name != "@everyone":
                    role_list.append(role.mention)
            rlb=" | ".join(role_list)
            created_timetuple = interaction.user.created_at.timetuple()
            joined_timetuple = interaction.user.joined_at.timetuple()
            embed=discord.Embed(title=f"{interaction.user.name} - Info",color=discord.Color.blue(),
                                timestamp=datetime.datetime.now())
            embed.add_field(name="アカウント作成日",
                            value=" | ".join([f"<t:{int(time.mktime(created_timetuple))}:R>",
                                              f"<t:{int(time.mktime(created_timetuple))}:D>"])
                                              )
            embed.add_field(name="アカウント参加日",
                            value=" | ".join([f"<t:{int(time.mktime(joined_timetuple))}:R>",
                                              f"<t:{int(time.mktime(joined_timetuple))}:D>"])
                                              )
            embed.add_field(name="ユーザーID",value=interaction.user.id,inline=False)
            embed.add_field(name="アイコンURL",value=f"[ユーザーアバター URL]({interaction.user.avatar.url})")
            embed.add_field(name=f"ロール({len(interaction.user.roles)})",
                            value="".join([rlb]),inline=False)
            embed.set_author(icon_url=interaction.user.avatar.url,name=interaction.user.global_name)
            embed.set_footer(text=guild.name)
            embed.set_thumbnail(url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

        else:
            role_list=[]
            for role in user.roles:
                if role.name != "@everyone":
                    role_list.append(role.mention)
            rlb=" | ".join(role_list)
            created_timetuple = user.created_at.timetuple()
            joined_timetuple = user.joined_at.timetuple()
            embed=discord.Embed(title=f"{user.name} - Info",color=discord.Color.blue(),
                                timestamp=datetime.datetime.now())
            embed.add_field(name="アカウント作成日",
                            value=" | ".join([f"<t:{int(time.mktime(created_timetuple))}:R>",
                                              f"<t:{int(time.mktime(created_timetuple))}:D>"])
                                              )
            embed.add_field(name="アカウント参加日",
                            value=" | ".join([f"<t:{int(time.mktime(joined_timetuple))}:R>",
                                              f"<t:{int(time.mktime(joined_timetuple))}:D>"])
                                              )
            embed.add_field(name="ユーザーID",value=user.id,inline=False)
            embed.add_field(name="アイコンURL",value=f"[ユーザーアバター URL]({user.avatar.url})")
            embed.add_field(name=f"ロール({len(user.roles)})",value="".join([rlb]),inline=False)
            embed.set_author(icon_url=user.avatar.url,name=user.global_name)
            embed.set_footer(text=guild.name)
            embed.set_thumbnail(url=user.avatar.url)

            await interaction.response.send_message(embed=embed)

class Mod(commands.GroupCog):
    """ModCommands Class

        Its function will be registered when bot will start
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="指定したメンバーをBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(days="BANしたユーザーのメッセージ削除の期間")
    async def ban(self,
                  interaction: discord.Interaction,
                  member: discord.Member,
                  reason: str = "無し", days: int = 0):
        """When user use /member ban,Invoke this

        Args:
            interaction (discord.Interaction): None desctiption
            member (discord.Member): member object in discord
            reason (str, optional): string of ban reason. Defaults to "無し".
            days (int, optional): int of days in delete messages. Defaults to 0.
        """
        await member.ban(reason=reason, delete_message_days=days)
        await interaction.response.send_message(embed=embeds.gen_managelog(
            member.display_name,
            interaction.user.mention,
            "BAN",
            reason,
            interaction.guild.name
            ))

    @app_commands.command(description="指定したメンバーをグローバルBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(days="BANしたユーザーのメッセージ削除の期間")
    async def gban(self, interaction: discord.Interaction, member: discord.Member,
                   reason: str = "無し", days: int = 0):
        """When user use /member gban,Invoke this

        Args:
            interaction (discord.Interaction): None desctiption
            member (discord.Member): member object in discord
            reason (str, optional): string of global ban reason. Defaults to "無し".
            days (int, optional): int of days in delete messages. Defaults to 0.
        """
        if not member.id in user_karma_list:
            user_karma_list[member.id] = 0
        user_karma_list[member.id] -= 1

        await member.ban(reason=reason, delete_message_days=days)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name,
                                                                           interaction.user.mention,
                                                                           "グローバルBAN",
                                                                           reason,
                                                                           interaction.guild.name
                                                                           ))

    @app_commands.command(description="指定したメンバーをKICKします")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member
                   ,reason: str = "無し"):
        """When user use /member kick,Invoke this

        Args:
            interaction (discord.Interaction): None desctiption
            member (discord.Member): member object in discord
            reason (str, optional): string of kick reason. Defaults to "無し".
        """
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name,
                                                                           interaction.user.mention,
                                                                           "kick",
                                                                           reason,
                                                                           interaction.guild.name
                                                                           ))

    @app_commands.command(description="指定したメンバーをunBANします")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: discord.User,
                    reason: str = "無し"):
        """When user use /member unban,Invoke this

        Args:
            interaction (discord.Interaction): None desctiption
            member (discord.Member): member object in discord
            reason (str, optional): string of unban reason. Defaults to "無し".
        """
        guild = interaction.guild

        await guild.unban(user=member, reason=reason)
        await interaction.response.send_message(embed=embeds.gen_managelog(member.display_name,
                                                                           interaction.user.mention,
                                                                           "unBAN",
                                                                           reason,
                                                                           interaction.guild.name
                                                                           ))

class Log(commands.GroupCog):
    """LogChannelSelect Class

        Its function will be registered when bot will start
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="ログを取るためのチャンネルを設定します")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel="ログを取るチャンネル")
    async def channelselect(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """
        A command to set up log channel
        """
        bot_icon=await self.bot.user.avatar.read()
        webhook=await channel.create_webhook(
            name="CalicobotLog",avatar=bot_icon,reason="to get logs")
        await interaction.response.send_message(f":white_check_mark:`{webhook.name}`を作成しました!")

    @app_commands.command(description="ログを取っているチャンネルでログを取れなくします")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel="ログを取っているチャンネル")
    async def channeldelete(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """
        A command to delete exist log channel
        """
        delete_webhooks = filter(
            lambda webhook: webhook.name == "CalicobotLog",
            await channel.webhooks()
        )
        for webhook in delete_webhooks:
            await webhook.delete()
            await interaction.response.send_message(
                f":white_check_mark:`{webhook.name}`を削除し\nログを取れなくました")

async def setup(bot):
    """
    Call when execution bot's reload commands or bot's status is ready
    """
    await bot.add_cog(Member(bot))
    await bot.add_cog(Mod(bot))
    await bot.add_cog(Log(bot))
    await bot.tree.sync()
