import telebot
import datetime
import os
import json
from dotenv import load_dotenv
from functions import typing, start_buttons

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    cht = message.chat.id
    username = message.from_user.username

    if username == None:
        typing(bot, cht, 'Схоже, у тебе не встановлене <b>Ім\'я користувача</b>\nЙого необхідно встановити, щоб користуватись нашим сервісом')
    else:
        with open('users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if username not in data:
            time_now = datetime.datetime.now()
            date = time_now.strftime('%d.%m.%Y, %H:%M:%S')

            data[username] = {
                'join_date': date
            }
            with open('users.json', 'w', encoding='utf-8') as f2:
                json.dump(data, f2, ensure_ascii=False)

            typing(bot, cht, 'Привіт 👋\nГайда реєструватись та ділитсь найяскравішими мометами з друзями 📸')
            typing(bot, cht, 'Давай заповнимо профіль!\nНадішли гарненьку аватарку ;)', next_func=get_avatar)
        else:
            typing(bot, cht, 'Привіт 👋\nПублікуємо нове фото?)', markup='start')

def get_avatar(message):
    cht = message.chat.id
    username = message.from_user.username

    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        save_path = os.path.join('images', f'{message.from_user.username}.jpg')
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        with open('users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        data[username]['image_path'] = f'images/{message.from_user.username}.jpg'
        
        with open('users.json', 'w', encoding='utf-8') as f2:
            json.dump(data, f2, ensure_ascii=False)
        
        typing(bot, cht, 'Люкс 😻\nРухаємось далі!')
        typing(bot, cht, 'Тепер напиши який-небудь опис 💬\nРозкажи, наприклад, хто ти/що будеш публікувати...', get_description)
    except Exception as ex:
        typing(bot, cht, 'Халепа! Спробуй ще раз, або звернись у підтримку')
        typing(bot, cht, f'Помилка: {ex}', get_avatar)

def get_description(message):
    cht = message.chat.id
    username = message.from_user.username
    description = message.text

    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        data[username]['description'] = f'{description}'
        
        with open('users.json', 'w', encoding='utf-8') as f2:
            json.dump(data, f2, ensure_ascii=False)
        
        typing(bot, cht, 'Супер 👍\nУсе готово для першої публікації 😉', markup='start')
    except Exception as ex:
        typing(bot, cht, 'Халепа! Спробуй ще раз, або звернись у підтримку')
        typing(bot, cht, f'Помилка: {ex}', get_description)

@bot.message_handler(content_types=['text'])
def text(message: telebot.types.Message) -> None:
    cht = message.chat.id
    username = message.from_user.username

    if message.text == 'Профіль 👤':
        with open(f'users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            bot.send_photo(cht, open(os.path.join(data[username]['image_path']), 'rb'),
                           caption=f'<blockquote><b>{data[username]['description']}</b></blockquote>\n' +
                           f'Приєднання: <b>{data[username]['join_date']}</b>',
                           parse_mode='HTML')

bot.polling()