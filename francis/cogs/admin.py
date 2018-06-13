from pprint import pprint

import asyncio
import operator
import os

import discord
from discord.ext import commands

import config

# francis/cogs/here -> francis/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Admin:
    """A cog for Admin-only commands"""

    def __init__(self, bot, util):
        self.bot = bot
        self.util = util

    def is_me(ctx):
        return ctx.message.author.id == config.MY_ID

    @commands.command(pass_context=True, name='clear')
    @commands.check(is_me)
    async def clear_messages(self, context, limit=100, check=None):
        """Lệnh xóa tin nhắn
        """
        channel = context.message.channel

        if check is None:
            messages = []
            async for message in self.bot.logs_from(channel, limit=limit):
                messages.append(message)

            note = await self.bot.say(f'Tiến hành xóa {len(messages)} tin nhắn :hourglass_flowing_sand:')
            chunks = [messages[x:x + 100] for x in range(0, len(messages), 100)]
            counter = 0
            for chunk in chunks:
                await self.bot.delete_messages(chunk)
                counter += len(chunk)
                if chunk != chunks[-1]:
                    await self.bot.edit_message(
                        note,
                        f'Xóa thành công {counter}/{len(messages)} tin nhắn :hourglass_flowing_sand:')
                else:
                    end_note = await self.bot.edit_message(
                        note,
                        f'Xóa thành công {counter}/{len(messages)} tin nhắn :white_check_mark:\n'
                        '*Tự động xóa tin nhắn này sau 10 giây*')
                    print(f'Deleted {counter}/{len(messages)} messages.')

            await asyncio.sleep(10)
            await self.bot.delete_message(end_note)

        else:

            def is_me(m):
                return m.author == self.bot.user

            deleted = await self.bot.purge_from(channel, limit=limit, check=is_me)
            await self.bot.say(f'Deleted {len(deleted)} message(s)')

    @clear_messages.error
    async def clear_messages_error(self, error, context):

        print(f'@{context.message.author.name} (ID: {context.message.author.id}) tried to clear messages.')
        pass  # fail silently

    @commands.command(pass_context=True, name='countmsg')
    @commands.check(is_me)
    async def count_users_messages(self, context, prefix=None, limit=5000):
        """Lệnh đếm số tin nhắn trong kênh
        Nếu có 'prefix', chỉ đếm những tin nhắn có prefix.
        KHÔNG đếm những tin nhắn của bot (có role Artificial Intelligence)
        """

        channel = context.message.channel
        ai_role = discord.utils.get(context.message.server.roles, name='Artificial Intelligence')

        note = await self.bot.say(f'Đang xử lý...')
        counter = 0
        data_dict = {}
        async for message in self.bot.logs_from(channel, limit=limit):

            # excludes bot (Bot with Artificial Intelligence Role)
            if ai_role not in message.author.roles:

                # prefix counter
                if prefix is not None:
                    if message.content.startswith(prefix):
                        if message.author.name in list(data_dict.keys()):
                            data_dict[message.author.name] += 1
                        else:
                            data_dict.update({message.author.name: 1})
                        counter += 1
                # no prefix
                else:
                    if message.author.name in list(data_dict.keys()):
                        data_dict[message.author.name] += 1
                    else:
                        data_dict.update({message.author.name: 1})
                    counter += 1

        sorted_data = sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True)

        embed = discord.Embed(
            title='Kết quả',
            description=f'Tổng số tin nhắn được xử lý: `{counter}`',
            color=discord.Color.teal())

        for index, item in enumerate(sorted_data, start=1):
            if index == 1:
                rank_indicator = ':first_place:'
            elif index == 2:
                rank_indicator = ':second_place:'
            elif index == 3:
                rank_indicator = ':third_place:'
            elif index in [4, 5]:
                rank_indicator = ':ribbon:'
            else:
                rank_indicator = ''
            embed.add_field(
                name=f'{item[0]} {rank_indicator}',
                value=f'Số tin nhắn: `{item[1]}`')

        await self.bot.delete_message(note)
        await self.util.say_as_embed(embed=embed)

    @commands.command(pass_context=True, name='playing')
    @commands.check(is_me)
    async def change_bot_presence(self, context, presence: str):
        await self.bot.change_presence(game=discord.Game(name=presence))