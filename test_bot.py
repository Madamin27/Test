

import telebot
import sqlite3


token = '7172929869:AAFD9rxdR5gJZGKIbWUn6M352X4HiU_qjmc'


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER name varchar(50),password varchar(50));''')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Username kiriting')
    bot.register_next_step_handler(message, user_name,)

name = ''
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id,'Parolni kiriting')
    bot.register_next_step_handler(message, user_password)

def user_password(message):
    password = message.text.strip()
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    data = (f"{name}", F"{password}")
    cur.execute(f"INSERT INTO user (name, password) VALUES {data}")
    conn.commit()
    cur.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Userlar ro'yxati", callback_data='user'))
    bot.send_message(message.chat.id, "Ro'yxatdan o'tildi", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f"Ism {el[1]} Parol {el[2]}"

    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)

print("The bot is running...")
bot.polling(none_stop=True)
