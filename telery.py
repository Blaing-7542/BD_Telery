import wikipediaapi
from pyrogram import Client, filters
import random
import asyncio
import time
import requests
import io
import os
from pyrogram.errors import FloodWait
import wikipedia

with open("info.openme", "r") as file:
    lines = file.readlines()
    api_id = int(lines[0].strip())
    api_hash = lines[1].strip()
    userid_telegram = int(lines[2].strip())
app = Client("my_account", api_id=api_id, api_hash=api_hash)
wiki_wiki = wikipediaapi.Wikipedia(
    language='ru',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='TeleryUserBot/1.0'
)

open("bldb.txt", "a").close()

with open("bldb.txt", "r") as file:
    for line in file:
        user_id = int(line.strip())
        blacklist.append(user_id)

response = requests.get("https://raw.githubusercontent.com/Blaing7542/Assis-userbot/main/bull_db")
if response.status_code == 200:
    bull_variants = [line.strip() for line in io.StringIO(response.text)]
else:
    bull_variants = ["Нет доступа к сайту с базой данных __.bull__"]

@app.on_message(filters.command("help", prefixes="."))
async def help_command(_, message):
    await message.edit_text("**Команды:**\n`.bull` - буллинг\n`.info` - инфо о юб\n`.doubletext` - удваивает текст. пример: *ппррииввеетт!*\n`.math` - решает математические задачи\n`.caz` - делает ставку на что-угодно. пример: *.caz 2 доллара*\n`.addbl` - добавить пользователя в чёрный список. Он не сможет пользоваться командами вашего юб.\n`.delbl` - удалить пользователя из чёрного списка.\n`.animtext` - анимирует текст.\n`.ab` - автоматический буллинг\n`delab` - убрать из автоматического булла.\n`.who` - выбирает рандомного чела, и пишет кто он.\n`.randkomaru` - кидает рандомную гифку с Комару\n`.oorr` - Орёл или решка\n`.ping` - Пишет пинг юб.\n`.math` - Решает математические задачи\n`.time` - Показывает время пользователя юб.\n`.search` - Ищет информацию в интернете.\n`.chebupelka`(локальная команда) - Команда просто пишет *Чебупельку ебали*\n`.cuword` - Отправляет милое предложение")

@app.on_message(filters.command("bull", prefixes="."))
async def bull_command(_, message):
    if message.from_user.id in blacklist:
        await message.reply_text("Вы находитесь в чёрном списке.")
        return

    await message.edit_text(random.choice(bull_variants))

@app.on_message(filters.command("info", prefixes="."))
async def info_command(_, message):
    user_id = message.from_user.id
    with open("bldb.txt", "r") as file:
        allowed_ids = file.read().splitlines()
    if str(user_id) in allowed_ids:
        await message.reply_text("Вам запрещено использовать эту команду.")
    else:
        start_time = time.time()
        await message.delete()
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 1)
        await app.send_photo(
            chat_id=message.chat.id,
            photo="https://user-images.githubusercontent.com/149149385/278584536-1dab252e-9fd4-4a0c-a80e-5e16c1220eaa.jpg",
            caption=f"**✨Telery**\n__🔧Version: 1.5__\nSource: https://t.me/telery_userbot\n**Version for user❤**\n**Ping: {ping_time}ms**"
        )


@app.on_message(filters.command("doubletext", prefixes="."))
async def animtext_command(_, message):
    user_id = message.from_user.id
    with open("bldb.txt", "r") as file:
        if str(user_id) in file.read():
            await message.reply("Вам запрещено использовать эту команду.")
            return

    text = message.text.split(".doubletext ", 1)[1]
    animated_text = ""
    for char in text:
        animated_text += char + char
    await message.edit_text(animated_text)

@app.on_message(filters.command("caz", prefixes="."))
async def caz_command(_, message):
    await asyncio.sleep(4)
    bet = message.text.split(".caz ", 1)[1]
    try:
        bet_amount, bet_text = bet.split(maxsplit=1)
        bet_amount = int(bet_amount)
        if bet_amount <= 0:
            await message.reply_text("Ставка должна быть положительным числом!")
            return
    except (ValueError, IndexError):
        await message.reply_text("Некорректная ставка!")
        return

    result = random.choice([0, 1])
    if result == 0:
        loss_amount = bet_amount
        await message.reply_text(f"Проигрыш! Вы проиграли {loss_amount} {bet_text}")
    else:
        win_amount = bet_amount * 2
        await message.reply_text(f"Выигрыш! Вы выиграли {win_amount} {bet_text}")

@app.on_message(filters.command("addbl", prefixes="."))
async def add_blacklist_command(_, message):
    if message.from_user.id == userid_telegram:
        user_id = message.reply_to_message.from_user.id
        if user_id not in blacklist:
            blacklist.append(user_id)
            with open("bldb.txt", "a") as file:
                file.write(str(user_id) + "\n")
            await message.reply_text("Пользователь добавлен в чёрный список. Теперь пользователь не может использовать все команды вашего юб.")
        else:
            await message.reply_text("Пользователь уже находится в чёрном списке.")
    else:
        await message.reply_text("У вас нет разрешения на использование этой команды.")

@app.on_message(filters.command("delbl", prefixes="."))
async def remove_blacklist_command(_, message):
    if message.from_user.id == userid_telegram:
        user_id = message.reply_to_message.from_user.id
        if user_id in blacklist:
            blacklist.remove(user_id)
            with open("bldb.txt", "w") as file:
                for id in blacklist:
                    file.write(str(id) + "\n")
            await message.reply_text("Пользователь удален из чёрного списка.")
        else:
            await message.reply_text("Пользователь не найден в чёрном списке.")
    else:
        await message.reply_text("У вас нет разрешения на использование этой команды.")

@app.on_message(filters.command("animtext", prefixes='.') & filters.me)
async def animtext_command(_, message):
    input_text = message.text.split(".animtext ", maxsplit=1)[1]
    temp_text = input_text
    edited_text = ""
    typing_symbol = "█"

    while edited_text != input_text:
        try:
            await message.edit(edited_text + typing_symbol)
            time.sleep(0.1)
            edited_text = edited_text + temp_text[0]
            temp_text = temp_text[1:]
            await message.edit(edited_text)
            time.sleep(0.1)
        except FloodWait:
            print("Превышен лимит сообщений в секунду. Подождите...")


@app.on_message(filters.command("ab", prefixes="."))
def enable_auto_bull(client, message):
    user_id = message.from_user.id
    with open("user_id.txt", "r") as file:
        allowed_user_id = file.read().strip()
    if str(user_id) != allowed_user_id:
        message.reply("Вам запрещено использовать эту команду.")
        return
    message.reply("Автобулл включён.")
    with open("ab.txt", "a") as file:
        file.write(f"{user_id}\n")

@app.on_message(filters.command("delab", prefixes="."))
def delab_command(client, message):
    user_id_to_remove = message.reply_to_message.from_user.id
    with open("user_id.txt", "r") as file:
        user_ids = file.read().splitlines()
    if str(user_id_to_remove) not in user_ids:
        message.reply_text("Вам запрещено использовать эту команду.")
        return
    user_ids = [user_id for user_id in user_ids if user_id != str(user_id_to_remove)]
    with open("user_id.txt", "w") as file:
        file.write("\n".join(user_ids))
    message.reply_text("**Пользователь удален из списка автобулл.**")



@app.on_message(filters.command("who", prefixes="."))
def who_command(client, message):
    args = message.text.split()[1:]
    if args:
        members_count = client.get_chat_members_count(message.chat.id)
        members = client.get_chat_members(message.chat.id, limit=members_count)
        random_user = random.choice(list(members)).user
        response = f"@{random_user.username} {' '.join(args)}"
    else:
        response = "Неверно написано. Пример:\n`.who милый`"
    with open("bldb.txt", "r") as file:
        banned_users = file.read().splitlines()
    if str(message.from_user.id) in banned_users:
        response = "Вам запрещено использовать эту команду."
    client.send_message(message.chat.id, response)


@app.on_message(filters.command('randkomaru', prefixes='.'))
async def send_random_komaru_gif(client, message):
    user_id = message.from_user.id
    with open('bldb.txt', 'r') as file:
        if str(user_id) in file.read():
            await message.reply('Вам запрещено использовать эту команду.')
            return

    url = 'https://raw.githubusercontent.com/Blaing-7542/BD_Telery/main/komarugifbd'
    response = requests.get(url)
    if response.status_code == 200:
        gifs = response.text.split('\n')
        random_gif = random.choice(gifs)
        await message.reply_animation(random_gif)
    else:
        await message.reply('Не удалось получить гифку. Попробуйте позже.')

@app.on_message(filters.command("oorr", prefixes="."))
def oorr_command(client, message):
    user_id = message.from_user.id
    with open("bldb.txt", "r") as file:
        banned_users = file.read().splitlines()

    if str(user_id) in banned_users:
        message.reply_text("Вам запрещено использовать эту команду.")
        return

    random_number = random.randint(0, 1)
    if random_number == 0:
        coin_emoji = "🌑"
        result = "Выпал орёл!"
    else:
        coin_emoji = "🌑"
        result = "Выпала решка!"

    message.reply_text(coin_emoji)
    time.sleep(2)
    message.reply_text(result)

@app.on_message(filters.command("ping", prefixes="."))
def ping(_, message):
    with open("bldb.txt", "r") as file:
        user_ids = file.read().splitlines()
        if str(message.from_user.id) in user_ids:
            message.reply("Вам запрещено использовать эту команду.")
        else:
            start_time = time.time()
            msg = message.edit("🌕")
            end_time = time.time()
            ping_time = round((end_time - start_time) * 1000)
            msg.edit("**🕛Ваш пинг: {} мс**".format(ping_time))

@app.on_message(filters.command("time", prefixes="."))
def send_time(client, message):
    user_id = message.from_user.id
    with open("bldb.txt", "r") as file:
        banned_users = [int(line.strip()) for line in file]
    if user_id in banned_users:
        message.reply_text("Вам запрещено использовать эту команду.")
    else:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        message.reply_text(f"⌛Время пользователя: {current_time}")

@app.on_message(filters.command("math", prefixes="."))
def calculate_math(client, message):
    user_id = str(message.from_user.id)
    if user_id in open("bldb.txt").read():
        message.reply("Вам запрещено использовать эту команду.")
    else:
        command = message.text.split(" ", 1)[1]
        if command.startswith(("exit", "dir")):
            message.reply("Такие слова писать запрещено!")
        else:
            try:
                result = eval(command)
                message.reply(f"{command} = {result}")
            except Exception as e:
                message.reply(f"Произошла ошибка: {str(e)}")


@app.on_message(filters.command("search", prefixes="."))
def search_command(client, message):
    user_id = message.from_user.id
    with open("bldb.txt", "r") as file:
        if str(user_id) in file.read():
            message.edit_text("Вам запрещено использовать эту команду.")
        else:
            query = message.text.split(' ', 1)[1]
            page_py = wiki_wiki.page(query)
            if page_py.exists():
                response = "**🧠Нашёл ответ:**\n\n" + page_py.text[:1024]
                message.edit_text(response)
            else:
                message.edit_text("Статья не найдена на Википедии.")

@app.on_message(filters.text & filters.private)
def auto_bull(_, message):
    user_id = message.from_user.id
    with open("ab.txt", "r") as file:
        user_ids = file.read().splitlines()

    if str(user_id) in user_ids:
        response = requests.get("https://raw.githubusercontent.com/Blaing7542/Assis-userbot/main/bull_db")
        if response.status_code == 200:
            sentences = response.text.splitlines()
            random_sentence = random.choice(sentences)
            message.reply(random_sentence)

@ app.on_message(filters.text & filters.command("chebupelka", prefixes="."))
def chebupelka_handler(client, message):
    message.edit("❤чебупельку ебали❤(добавил @Not_A_Altuskha)")

@ app.on_message(filters.command("cuword", prefixes="."))
def change_message(client, message):
    response = requests.get("https://raw.githubusercontent.com/Blaing-7542/BD_Telery/main/cute-words-bd")
    cute_words = response.text.splitlines()
    random_cute_word = random.choice(cute_words)
    message.edit(random_cute_word)

app.run()
