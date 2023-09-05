import discord
import datetime
from discord.ext import commands
from discord import app_commands
import time
import embeds
import main

bot=commands.Bot(command_prefix="t?",intents=discord.Intents.all())

user_karma_list = main.user_karma_list

class MemberCommands(app_commands.Group):
    """MemberCommands Class

        Its function will be registered when bot will start
    """

    def __init__(self, name: str):
        super().__init__(name=name)
    @app_commands.command(description="サーバーの情報を表示します")
    async def serverinfo(self, interaction: discord.Interaction):
        guild=interaction.guild
        guildOnlineMember=0
        for onlineMember in guild.members:
            if onlineMember.status == discord.Status.online:
                guildOnlineMember + 1

        roleList=[]
        for role in guild.roles:
            roleList.append(role.mention)
        rlb=" | ".join(roleList)
        embed=discord.Embed(title=f"{guild.name} - Info",color=discord.Color.blue(),timestamp=datetime.datetime.now())
        embed.add_field(name="作成日",value=f"<t:{int(time.mktime(guild.created_at.timetuple()))}:R>")
        embed.add_field(name="サーバーID",value=f"{guild.id}")
        embed.add_field(name="所有者",value=guild.owner.mention)
        embed.add_field(name=f"メンバー数({guild.member_count})",value=f"**{str(guildOnlineMember)}** オンライン\n**{guild.premium_subscription_count}** ブースター")
        embed.add_field(name=f"チャンネル数({len(guild.channels)})",value=f"**{len(guild.text_channels)}** テキストチャンネル\n**{len(guild.voice_channels)}** ボイスチャンネル")
        embed.add_field(name=f"ロール({len(guild.roles)})",value="".join([rlb]),inline=False)
        embed.set_author(icon_url=interaction.user.avatar.url,name=interaction.user.global_name)
        embed.set_footer(text=guild.name)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="指定したユーザーの情報を表示します")
    @app_commands.describe(user="情報を表示したいユーザーを指定します")
    async def info(self, interaction: discord.Interaction, user: discord.Member = None):
        guild=interaction.guild

        if user == None:
            roleList=[]
            for role in interaction.user.roles:
                if role.name != "@everyone":
                    roleList.append(role.mention)
            rlb=" | ".join(roleList)
            embed=discord.Embed(title=f"{interaction.user.name} - Info",color=discord.Color.blue(),timestamp=datetime.datetime.now())
            embed.add_field(name="アカウント作成日",value=f"<t:{int(time.mktime(interaction.user.created_at.timetuple()))}:R> | <t:{int(time.mktime(interaction.user.created_at.timetuple()))}:D>")
            embed.add_field(name="アカウント参加日",value=f"<t:{int(time.mktime(interaction.user.joined_at.timetuple()))}:R> | <t:{int(time.mktime(interaction.user.joined_at.timetuple()))}:D>")
            embed.add_field(name="ユーザーID",value=interaction.user.id,inline=False)
            embed.add_field(name="アイコンURL",value=f"[ユーザーアバター URL]({interaction.user.avatar.url})")
            embed.add_field(name=f"ロール({len(interaction.user.roles)})",value="".join([rlb]),inline=False)
            embed.set_author(icon_url=interaction.user.avatar.url,name=interaction.user.global_name)
            embed.set_footer(text=guild.name)
            embed.set_thumbnail(url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

        else:
            roleList=[]
            for role in user.roles:
                if role.name != "@everyone":
                    roleList.append(role.mention)
            rlb=" | ".join(roleList)
            embed=discord.Embed(title=f"{user.name} - Info",color=discord.Color.blue(),timestamp=datetime.datetime.now())
            embed.add_field(name="アカウント作成日",value=f"<t:{int(time.mktime(user.created_at.timetuple()))}:R> | <t:{int(time.mktime(user.created_at.timetuple()))}:D>")
            embed.add_field(name="アカウント参加日",value=f"<t:{int(time.mktime(user.joined_at.timetuple()))}:R> | <t:{int(time.mktime(user.joined_at.timetuple()))}:D>")
            embed.add_field(name="ユーザーID",value=user.id,inline=False)
            embed.add_field(name="アイコンURL",value=f"[ユーザーアバター URL]({user.avatar.url})")
            embed.add_field(name=f"ロール({len(user.roles)})",value="".join([rlb]),inline=False)
            embed.set_author(icon_url=user.avatar.url,name=user.global_name)
            embed.set_footer(text=guild.name)
            embed.set_thumbnail(url=user.avatar.url)

            await interaction.response.send_message(embed=embed)

class ModCommands(app_commands.Group):
    """ModCommands Class

        Its function will be registered when bot will start
    """

    def __init__(self, name: str):
        super().__init__(name=name)

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

class logChannelSelect(app_commands.Group):
    """logChannelSelect Class

        Its function will be registered when bot will start
    """

    def __init__(self, name: str):
        super().__init__(name=name)
    @app_commands.command(description="ログを取るためのチャンネルを設定します")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel="ログを取るチャンネル")
    async def channelselect(self, interaction: discord.Interaction, channel: discord.TextChannel):
        botIcon=await bot.user.avatar.read()
        webhook=await channel.create_webhook(name="CalicobotLog",avatar=botIcon,reason="to get logs")
        await interaction.response.send_message(f":white_check_mark:`{webhook.name}`を作成しました!")

    @app_commands.command(description="ログを取っているチャンネルでログを取れなくします")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel="ログを取っているチャンネル")
    async def channeldelete(self, interaction: discord.Interaction, channel: discord.TextChannel):
        webhooks=await channel.webhooks()
        for webhook in webhooks:
            if webhook.name == "CalicobotLog":
                await webhook.delete()
                await interaction.response.send_message(f":white_check_mark:`{webhook.name}`を削除し\nログを取れなくました")