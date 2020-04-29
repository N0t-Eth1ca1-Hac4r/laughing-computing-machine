import discord
from discord.ext import commands
import datetime
from discord.utils import get
import requests
import json
import os

# Переменные (токен и префикс)
prefix = '$'
token = os.environ.get('BOT_TOKEN')
client = commands.Bot(command_prefix = prefix)
client.remove_command('help')

# Авто-выдача роли
@client.event

async def on_member_join(member):
    channel = client.get_channel(704269121159692339)
    role = discord.utils.get(member.guild.roles, id = 704439326083383358)
    await member.add_roles(role)
    await channel.send(embed = discord.Embed(description = f'Пользователь {member.mention} присоединился к нам! Напиши "$help" без кавычек!', color = 0x39d0d6))

# Проверка работоспособности бота
@client.event

async def on_ready():
    print('Bot is connected')

    await client.change_presence(status = discord.Status.online, activity = discord.Game('Detroit: Become Human'))

# Команды с правами админа

# Очистка чата
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)

# Кик
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = 'Ничего не знаю, я бот'):
    emb = discord.Embed(title = 'Kick', colour = discord.Color.red())
    await member.kick(reason = reason)
    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
    emb.set_footer(text='User has been kicked from {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed = emb)

# Бан
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = 'Ничего не знаю, ибо я бот. Но хозяин тебя забанил.'):
    emb = discord.Embed(title = 'Ban', colour = discord.Color.red())
    await member.ban(reason = reason)
    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = 'Ban user', value = 'Banned user : {}'.format(member.mention))
    emb.set_footer(text = 'User has been banned from {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
    await ctx.send(embed = emb)

# Разбан
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def pardon(ctx, *, member):
    emb = discord.Embed(title = 'UnBan', colour = discord.Color.green())
    banned = await ctx.guild.bans()
    for ban_entry in banned:
        user = ban_entry.user
        await ctx.guild.unban(user)
        emb.set_author(name = user.name, icon_url = user.avatar_url)
        emb.add_field(name = 'UnBan user', value = 'UnBanned user : {}'.format(user.mention))
        emb.set_footer(text='User has been unbanned from {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed = emb)

        return


# Обычные команды

# Приветствие
@client.command(pass_context = True)
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f' {author.mention} Привет!')

# Помощь (help)
@client.command(pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'Info about commands', colour = 0x39d0d6)
    emb.add_field(name = '{}kick'.format(prefix), value = 'Удаление участника с сервера (only adm) ')
    emb.add_field(name='{}ban'.format(prefix), value='Ограничение доступа к серверу (only adm) ')
    emb.add_field(name='{}pardon'.format(prefix), value='Снятие ограничения доступа к серверу (only adm) ')
    emb.add_field(name='{}clear'.format(prefix), value='Очистка чата (only adm) ')
    emb.add_field(name='{}hello'.format(prefix), value='Приветствие бота ')
    emb.add_field(name='{}time'.format(prefix), value='Показывает время ')
    emb.add_field(name='{}servinfo '.format(prefix), value='Показывает информацию о сервере ')
    emb.add_field(name='{}cov [ваша страна по английски без скобок]'.format(prefix), value='Показывает статистику о COVID-19 в выбранной стране ')
    await ctx.send(embed = emb)

# Время
@client.command(pass_context = True)
async def time(ctx):
    emb = discord.Embed(title = 'URL Time (click)', colour = 0x39d0d6, url = 'https://www.timeserver.ru/cities/ru/samara-russia')
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://psv4.userapi.com/c856424/u501822762/docs/d2/dc42743c00f5/suka.png')
    emb.set_thumbnail(url = 'https://psv4.userapi.com/c856424/u501822762/docs/d2/dc42743c00f5/suka.png')

    now_date = datetime.datetime.now()
    emb.add_field(name = 'Time', value = 'Time : {}'.format(now_date))

    await ctx.send(embed = emb)


# Информация о сервере
@client.command(pass_context = True)
async def servinfo(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион **{ctx.guild.region}\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: Онлайн: **{online}**\n\n"
        f":black_circle: Оффлайн: **{offline}**\n\n"
        f":yellow_circle: Отошли: **{idle}**\n\n"
        f":red_circle: Не трогать: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)


# COVID-19
@client.command(aliases=['коронавирус'])
async def cov(ctx, country):
    for item in json.loads(requests.get("http://covid2019-api.herokuapp.com/v2/current").text)['data']:
        if item['location'] == country:
            return await ctx.send(embed=discord.Embed(title='CoronaVirus Stat', description=f'Данные по {country}:\nУмерло: {item["deaths"]}\nВыздоровело: {item["recovered"]}\nЗаражено: {item["confirmed"]}'))

client.run(str(token))
