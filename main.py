from random import randint

import config
from discord import Intents, Game, Embed, Status, Member
from discord.ext import commands

try:
    intents = Intents().all()
    bot = commands.Bot(command_prefix="!", intents=intents,
                       activity=Game(name="!help"))
    bot.remove_command("help")


    @bot.command()
    async def help(ctx):
        emb = Embed(title="Информация о командах", color=randint(0, 16777215))
        emb.add_field(name=f"`{'!'}help` : ", value="Вызовет это меню", inline=False)
        emb.add_field(name=f"`{'!'}server` :", value="Информация о сервере", inline=False)
        emb.add_field(name=f"`{'!'}user` :", value="Информация о пользователе", inline=False)
        emb.add_field(name=f"`{'!'}send_all_servers text` :", value="Отправить сообщение во все привязынные каналы",
                      inline=False)
        emb.add_field(name=f"`{'!'}send_to_servers <id канала/ов> text` :",
                      value="Отправить сообщение в выбранные привязынные каналы",
                      inline=False)
        emb.add_field(name=f"`{'!'}add_chat id_чата/ов` :", value="Добавить канал/ы для отправки сообщений",
                      inline=False)
        emb.add_field(name=f"`{'!'}remove_chat id_чата/ов` :", value="Удалить канал/ы",
                      inline=False)
        emb.add_field(name=f"`{'!'}get_chats` :", value="Получить список привязанных каналов",
                      inline=False)
        emb.add_field(name=f"`{'!'}delete id_сообщения` :", value="Удалить сообщение из всех привязынных каналов",
                      inline=False)
        emb.add_field(name=f"`{'!'}edit id_сообщения text` :",
                      value="Отпредактировать сообщение во всех привязынных каналах", inline=False)
        await ctx.reply(embed=emb, mention_author=False)


    @bot.command()
    async def send_all_servers(ctx):
        chat = ctx.channel.id
        with open("settings.txt", "r+") as settings:
            data = list(map(int, settings.read().split()))
        if chat in data:
            file = open('losm.txt', 'a')  # открытие файла для хранения списка сообщений
            text = ctx.message.content.replace('!send_all_servers \n', '').replace('!send_all_servers\n', '').replace(
                '!send_all_servers ', '').replace('!send_all_servers', '')
            file.write(f"{ctx.message.id} {chat} {ctx.message.guild.id} \n")  # запись сообщения отправителя в файл
            for i in data:  # проход по всем чатам
                if i == chat:
                    continue
                channel = bot.get_channel(i)
                message = await channel.send(text)
                file.write(f"{message.id} {i} {message.guild.id} \n")  # запись сообщения получателя в файл
            file.write("\n")
            file.close()  # сохранение файла
        else:
            embed = Embed(title=f'**Ошибка**', color=randint(0, 16777215))
            embed.add_field(name="**У вашего сервера/канала нет полномочий**",
                            value="", inline=False)
            return await ctx.send(embed=embed)


    @bot.command()
    async def send_to_servers(ctx):
        chat = ctx.channel.id
        with open("settings.txt", "r+") as settings:
            data = list(map(int, settings.read().split()))
        if chat in data:
            file = open('losm.txt', 'a')  # открытие файла для хранения списка сообщений
            text = ctx.message.content.replace('!send_to_servers \n', '').replace('!send_to_servers\n', '').replace(
                '!send_to_servers ', '').replace('!send_to_servers', '').split(">")
            file.write(f"{ctx.message.id} {chat} {ctx.message.guild.id} \n")  # запись сообщения отправителя в файл
            for i in text[0].replace("<", "").split():  # проход по всем чатам
                if i == chat:
                    continue
                channel = bot.get_channel(int(i))
                message = await channel.send(" ".join(text[1:]))
                file.write(f"{message.id} {i} {message.guild.id} \n")  # запись сообщения получателя в файл
            file.write("\n")
            file.close()  # сохранение файла
        else:
            embed = Embed(title=f'**Ошибка**', color=randint(0, 16777215))
            embed.add_field(name="**У вашего сервера/канала нет полномочий**",
                            value="", inline=False)
            return await ctx.send(embed=embed)


    @bot.command()
    async def add_chat(ctx):
        text = ctx.message.content.replace('!add_chat ', '').replace('!add_chat', '').split()
        with open("settings.txt", "r+") as settings:
            data = settings.read().split()
            settings.seek(0)
            settings.truncate()
        for _ in text:
            data.append(_)
        with open("settings.txt", "w") as settings:
            settings.write(" ".join(data))
        embed = Embed(title=f'**Success**', color=randint(0, 16777215))
        return await ctx.send(embed=embed)


    @bot.command()
    async def get_chats(ctx):
        with open("settings.txt", "r+") as settings:
            data = list(map(int, settings.read().split()))
        text = ""
        for _ in data:
            text += f"{bot.get_channel(_).name}:\t`{_}`\n"
        embed = Embed(title=f'**Чаты**', color=randint(0, 16777215))
        embed.add_field(name=text, value="", inline=False)
        return await ctx.send(embed=embed)


    @bot.command()
    async def remove_chat(ctx):
        text = ctx.message.content.replace('!remove_chat ', '').replace('!remove_chat', '').split()
        with open("settings.txt", "r+") as settings:
            data = settings.read().split()
        for _ in text:
            data.pop(data.index(_))
        with open("settings.txt", "w") as settings:
            settings.write(" ".join(data))
        embed = Embed(title=f'**Success**', color=randint(0, 16777215))
        return await ctx.send(embed=embed)


    @bot.command()
    async def delete(ctx):
        chat = ctx.channel.id
        with open("settings.txt", "r+") as settings:
            data = list(map(int, settings.read().split()))
        if chat in data:
            # открытие файла с информацией о сообщениях и запись их в список python
            with open('losm.txt', 'r') as file:
                list_of_send_messages = [row.strip().split() for row in file]
                id = str(ctx.message.content).split()[1]  # получение id
                # поиск сообщения по id в списке list_of_send_messages
                for i in range(len(list_of_send_messages)):
                    try:
                        if list_of_send_messages[i] == [str(id), str(chat), str(ctx.message.guild.id)]:
                            ind_l = i
                            break
                    except:
                        continue
                else:
                    embed = Embed(title=f'**Ошибка**', color=randint(0, 16777215))
                    embed.add_field(name="**Сообщение не найдено или ваш сервер/канал не является его создателем **",
                                    value="", inline=False)
                    return await ctx.send(embed=embed)

            for _ in range(ind_l, len(list_of_send_messages)):
                if not list_of_send_messages[_]:
                    ind_r = _
                    break
            else:
                ind_r = len(list_of_send_messages) - 1
            # открытие файла/чтение файла/создание списка удаляемых строк
            with open("losm.txt", "r") as file:
                lines = file.readlines()
                del_lines = lines[ind_l:ind_r].copy()
                for _ in range(len(del_lines)):
                    del_lines[_].replace(" \n", "")
            # удаление строк с информацией об удаленных сообщениях
            with open("losm.txt", "w") as file:
                for line in lines:
                    if line not in del_lines:
                        file.write(line)
            # удаление сообщений из чатов
            for i in list_of_send_messages[ind_l:ind_r]:
                try:
                    message = await bot.get_guild(int(i[2])).get_channel(int(i[1])).fetch_message(int(i[0]))
                    await message.delete()
                except:
                    continue

            file.close()
        else:
            embed = Embed(title=f'**Ошибка**', color=randint(0, 16777215))
            embed.add_field(name="**У вашего сервера/канала нет полномочий**",
                            value="", inline=False)
            return await ctx.send(embed=embed)


    @bot.command()
    async def edit(ctx):
        chat = ctx.channel.id
        with open("settings.txt", "r+") as settings:
            data = list(map(int, settings.read().split()))
        if chat in data:
            # открытие файла с информацией о сообщениях и запись их в список python
            with open('losm.txt', 'r') as file:
                list_of_send_messages = [row.strip().split() for row in file]
                id = str(ctx.message.content).split()[1]  # получение id
                text = " ".join(ctx.message.content.split()[2:])  # получение текста сообщения
                # поиск сообщения по id в списке list_of_send_messages
                for _ in range(len(list_of_send_messages)):
                    try:
                        if list_of_send_messages[_] == [str(id), str(chat), str(ctx.message.guild.id)]:
                            ind_l = _
                            break
                    except:
                        continue
                else:
                    embed = Embed(title=f'**Ошибка**', color=randint(0, 16777215))
                    embed.add_field(
                        name="**Сообщение не найдено или ваш сервер/канал не является его создателем **",
                        value="", inline=False)
                    return await ctx.send(embed=embed)
            for _ in range(ind_l, len(list_of_send_messages)):
                if not list_of_send_messages[_]:
                    ind_r = _
                    break
            else:
                ind_r = len(list_of_send_messages) - 1

            # изменение сообщений в чатах
            for i in list_of_send_messages[ind_l:ind_r]:
                try:
                    message = await bot.get_guild(int(i[2])).get_channel(int(i[1])).fetch_message(int(i[0]))
                    await message.edit(content=text)
                except:
                    continue
        else:
            embed = Embed(title=f'**Ошибка**', color=randint(0, 16777215))
            embed.add_field(name="**У вашего сервера/канала нет полномочий**",
                            value="", inline=False)
            return await ctx.send(embed=embed)


    @bot.command()
    async def server(ctx):
        name = str(ctx.guild.name)

        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        date = str(ctx.guild.created_at).split()
        memberCount = str(ctx.guild.member_count)
        online_members = []
        offline_members = []

        for member in ctx.guild.members:
            if member.status is not Status.offline:
                online_members.append(member.name)
            else:
                offline_members.append(member.name)
        icon = str(ctx.guild.icon.url)

        embed = Embed(title=f'**Статистика сервера {name}**', color=randint(0, 16777215))
        embed.set_thumbnail(url=icon)
        embed.add_field(name="**Владелец: **", value=owner)
        embed.add_field(name="**Дата создания: **", value=date[0], inline=True)
        embed.add_field(name="**ID: **", value=id, inline=False)
        embed.add_field(name="**Участников: **", value=memberCount)
        embed.add_field(name="Онлайн: ", value=f'{len(online_members)}')

        await ctx.send(embed=embed)


    @bot.command()
    async def user(ctx, member: Member = None):
        if not member:
            name = ctx.message.author.name
            icon = str(ctx.message.author.avatar.url)
            userAddForServer = str(ctx.message.author.joined_at).split()
            userAddForDiscord = str(ctx.message.author.created_at).split()
        else:
            name = member.name
            icon = str(member.avatar.url)
            userAddForServer = str(member.joined_at).split()
            userAddForDiscord = str(member.created_at).split()

        embed = Embed(title=f'**{name}**', color=randint(0, 16777215))
        embed.set_thumbnail(url=icon)
        embed.add_field(name="**Присоединился к discord: **\n", value=f'`{userAddForDiscord[0]}`', inline=True)
        embed.add_field(name="**Присоединился к серверу: **\n", value=f'`{userAddForServer[0]}`', inline=True)

        await ctx.send(embed=embed)


    bot.run(config.token)

except Exception as e:
    print(e)

"""Вся информация о сообщениях хранится в текстовом файле losm.txt"""
