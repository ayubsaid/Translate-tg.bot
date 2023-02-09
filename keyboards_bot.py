from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils import LANGUAGE

def generate_language():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    languages = []
    for language in LANGUAGE.values():
        lang_button = KeyboardButton(text=language)
        languages.append(lang_button)


    markup.add(*languages)
    return markup
