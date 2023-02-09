import sqlite3
import telebot.types
from telebot import TeleBot
from telebot.types import Message
from keyboards_bot import generate_language
from googletrans import Translator


bot = TeleBot('5654168195:AAGLkV4O2F9Szr01F9O-LY4CFOFZ2tMQKIc')

@bot.message_handler(commands=['start'])
def welcome(message: Message):
    # print(message)
    user_id = message.from_user.id
    bot.send_message(user_id, f"""Assalomu aleykum botimizga hush kelipsiz""")
    # bot.send_sticker(user_id, 'CAACAgIAAxkBAAEGBuVjQXJNU4BNpQx-U-ZsoQYpuyIWHQACfAEAAvCpxA-rXmcH4RGcyyoE')

    choose_first_language(message)


def choose_first_language(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id,
                     f"""Hurmatli foydalanuchi qaysi tildan tarjima qilishni tanglang:""",
                     reply_markup=generate_language())
    bot.register_next_step_handler(msg, choose_second_language)


def choose_second_language(message: Message):
    user_id = message.from_user.id
    first_language = message.text
    msg = bot.send_message(user_id,
                     f"""Hurmatli foydalanuchi qaysi tilga tarjima qilishni tanglang:""",
                     reply_markup=generate_language())

    bot.register_next_step_handler(msg, ask_text, first_language)


def ask_text(message: Message, first_language):
    user_id = message.from_user.id
    # print(first_language)
    second_language = message.text
    # print(second_language)
    msg = bot.send_message(user_id,
                     f"""Tarjima qilishi kerek bolgan textni jonating:""",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, translate, first_language, second_language)


def translate(message: Message, first_language, second_language):
    user_id = message.from_user.id
    text = message.text
    translator = Translator()
    translated_text = translator.translate(src=first_language.split(' ')[0],
                                           dest=second_language.split(' ')[0],
                                           text=text).text
    # src = (Birinchi qaysi tildan tarjima qilinsh kerek bolganini ishorat etadd 'src')
    # dest = (Ikinchi qaysi tilga tarjima qilinsh kerek bolganini ishorat etadd 'dest')
    # text = (Tarjima qilinbolgan texti yokida sozni chiqarip berishni ishora etadi 'text')



    database = sqlite3.connect('translate.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO history(telegram_id, from_lang, to_lang, original_text, translate_text)
    VALUES (?,?,?,?,?)
    ''', (user_id, first_language, second_language, text, translated_text))

    database.commit()
    database.close()


    bot.send_message(user_id, translated_text)
    choose_first_language(message)





bot.polling(none_stop=True)



