from discord.ext import commands
import discord
import asyncio
import operator
# from pprint import pprint
from config import MY_ID


class Requirement:
    """Bộ lệnh xem các tiêu chí set role"""

    def __init__(self, bot, util):
        self.bot = bot
        self.util = util

    @commands.command(pass_context=True, name='req')
    async def requirement(self, context, category=None):
        """Lệnh xem tiêu chí set các Role:
        - Content Creator
        - Guild Leader
        - Trader
        """
        prefix = self.bot.command_prefix
        server = context.message.server

        gms_role = discord.utils.get(server.roles, name='GMS')
        gmsm_role = discord.utils.get(server.roles, name='GMSM')

        role_request_channel = discord.utils.get(server.channels, name='yêu-cầu-role')

        if category is None \
                or not category.startswith('trade') \
                and not category.startswith('lead') \
                and not category.startswith('creat'):
            embed = discord.Embed(
                title=None,
                description=None,
                color=discord.Color.teal())

            embed.add_field(
                name='Xem tiêu chí set Role @Guild Leader',
                value=f'`{prefix}req leader`', inline=False)
            embed.add_field(
                name='Xem tiêu chí set Role @Trader',
                value=f'`{prefix}req trader`', inline=False)
            embed.add_field(
                name='Xem tiêu chí set Role @Content Creator',
                value=f'`{prefix}req creator`', inline=False)

            embed.set_image(url='https://i.imgur.com/xTyqmzZ.jpg')

            await self.util.say_as_embed(embed=embed)

        elif category.startswith('lead'):

            leader_gms = discord.utils.get(server.roles, name='Guild Leader GMS')
            leader_gmsm = discord.utils.get(server.roles, name='Guild Leader GMSM')

            embed = discord.Embed(
                title=None,
                description=None,
                color=discord.Color.dark_magenta())

            embed.add_field(
                name='1. Tiêu chí set Role @Guild Leader',
                value=''
                f'» Tuân thủ nội quy của kênh #tuyển-mem-guild (nhập `{prefix}help leader` để xem).\n'
                f'» Là đại diện cho Guild, không nhất thiết phải là Chủ Guild.\n'
                f'» Cần có role {gms_role.mention} nếu yêu cầu role {leader_gms.mention}.\n'
                f'» Cần có role {gmsm_role.mention} nếu yêu cầu role {leader_gmsm.mention}.\n.')
            embed.add_field(
                name='2. Cách yêu cầu Role @Guild Leader',
                value=''
                f'» Di chuyển đến kênh {role_request_channel.mention}.\n'
                f'» Chat theo cú pháp `$Guild Leader GMS` nếu muốn có role {leader_gms.mention}.\n'
                f'» Chat theo cú pháp `$Guild Leader GMSM` nếu muốn có role {leader_gmsm.mention}.\n'
                '» Chờ duyệt.\n.')
            embed.add_field(
                name='3. Lý do yêu cầu thủ công',
                value=''
                f'» Không để xảy ra tình trạng "Người người leader, nhà nhà leader".\n')

            await self.util.say_as_embed(embed=embed)

        elif category.startswith('trade'):

            trader_gms = discord.utils.get(server.roles, name='Trader GMS')
            trader_gmsm = discord.utils.get(server.roles, name='Trader GMSM')

            embed = discord.Embed(
                title=None,
                description=None,
                color=discord.Color.dark_blue())

            embed.add_field(
                name='1. Tiêu chí set Role @Trader',
                value=''
                f'» Tuân thủ nội quy của kênh #mua-bán (nhập `{prefix}help trader` để xem).\n'
                f'» Hoạt động trong group được một thời gian nhất định (do người duyệt xác định).\n'
                f'» Cần có role {gms_role.mention} nếu yêu cầu role {trader_gms.mention}.\n'
                f'» Cần có role {gmsm_role.mention} nếu yêu cầu role {trader_gmsm.mention}.\n.')
            embed.add_field(
                name='2. Cách yêu cầu Role @Trader',
                value=''
                f'» Di chuyển đến kênh {role_request_channel.mention}.\n'
                f'» Chat theo cú pháp `$Trader GMS` nếu muốn có role {trader_gms.mention}.\n'
                f'» Chat theo cú pháp `$Trader GMSM` nếu muốn có role {trader_gmsm.mention}.\n'
                f'» Chờ duyệt.\n.')
            embed.add_field(
                name='3. Lý do yêu cầu thủ công',
                value=''
                f'» Hạn chế tình trạng vào kênh để lừa đảo, spam.\n'
                f'» Tương tác với Maplers khác sẽ dễ mua bán hơn.\n')

            await self.util.say_as_embed(embed=embed)

        elif category.startswith('creat'):

            creator_gms = discord.utils.get(server.roles, name='Content Creator GMS')
            creator_gmsm = discord.utils.get(server.roles, name='Content Creator GMSM')

            ponpon = self.bot.get_user_info(MY_ID)

            embed = discord.Embed(
                title=None,
                description=None,
                color=discord.Color.dark_teal())

            embed.add_field(
                name='1. Tiêu chí set Role @Content Creator',
                value=''
                f'» Tuân thủ nội quy của kênh #creator (nhập `{prefix}help creator` để xem).\n'
                f'» Cần có role {gms_role.mention} nếu yêu cầu role {creator_gms.mention}.\n'
                f'» Cần có role {gmsm_role.mention} nếu yêu cầu role {creator_gmsm.mention}.\n.')
            embed.add_field(
                name='2. Cách yêu cầu Role @Content Creator',
                value=''
                f'» Di chuyển đến kênh {role_request_channel.mention}.\n'
                f'» Chat theo cú pháp `$Content Creator GMS` nếu muốn có role {creator_gms.mention}.\n'
                f'» Chat theo cú pháp `$Content Creator GMSM` nếu muốn có role {creator_gmsm.mention}.\n'
                f'» Nhắn tin cho {ponpon.mention} kèm 1 nội dung muốn đăng vào kênh.\n'
                '» Chờ duyệt.\n.')
            embed.add_field(
                name='3. Lý do yêu cầu thủ công',
                value=''
                f'» Không phải ai cũng có khả năng viết nội dung.\n'
                f'» Những Maplers thực sự muốn góp công xây dựng cộng đồng MapleStory VN lớn mạnh hơn mới dám bỏ thời gian ra '
                'làm hết những yêu cầu trên.\n')

            await self.util.say_as_embed(embed=embed)