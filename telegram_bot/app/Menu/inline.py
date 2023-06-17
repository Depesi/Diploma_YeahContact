from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import random


cf = CallbackData('post', 'id', 'action')


def inline_for_number(number_url, number_id):
    keyboard = InlineKeyboardMarkup()

    # but_open_in_web = InlineKeyboardButton("Відкрити в 🌐", url=number_url)
    but_add_comment = InlineKeyboardButton("Добавити 💬", callback_data=cf.new(id=number_id, action="comment"))
    but_view_comment = InlineKeyboardButton("Переглянути відгуки🔍",
                                            callback_data=cf.new(id=number_id, action="comment_view"))
    keyboard.add(but_view_comment)
    keyboard.add(#but_open_in_web,#
	 but_add_comment)
    return keyboard


def inline_for_number_with_comment(number, markup):
    keyboard = markup
    but_1 = InlineKeyboardButton("Небезпечний 🔴", callback_data=cf.new(id=f"{number}.1", action="comment_add"))
    but_2 = InlineKeyboardButton("Надокучливий 🟠", callback_data=cf.new(id=f"{number}.2", action="comment_add"))
    but_3 = InlineKeyboardButton("Нейтральний 🟡", callback_data=cf.new(id=f"{number}.3", action="comment_add"))
    but_4 = InlineKeyboardButton("Безпечний 🟢", callback_data=cf.new(id=f"{number}.4", action="comment_add"))

    keyboard.add(but_1)
    keyboard.add(but_2)
    keyboard.add(but_3)
    keyboard.add(but_4)
    return keyboard


def inline_for_view_comment(id_number, offset, max_comment):
    keyboard = InlineKeyboardMarkup()

    but_next = InlineKeyboardButton("➡️",
                                    callback_data=cf.new(id=f"{id_number}.{offset}", action="comment_view_next"))
    but_back = InlineKeyboardButton("⬅️",
                                    callback_data=cf.new(id=f"{id_number}.{offset}", action="comment_view_back"))
    but_text = InlineKeyboardButton(f"{offset+1}/{max_comment}",
                                    callback_data=cf.new(id=f"{id_number}.{offset}", action="comment_view_text"))

    keyboard.add(but_back, but_text, but_next)
    return keyboard


def inline_for_view_qa(offset, max_qa):
    keyboard = InlineKeyboardMarkup()

    but_next = InlineKeyboardButton("➕",
                                    callback_data=cf.new(id=f"'qa'.{offset}", action="qa_view_next"))
    but_back = InlineKeyboardButton("➖",
                                    callback_data=cf.new(id=f"'qa'.{offset}", action="qa_view_back"))
    but_text = InlineKeyboardButton(f"{offset+1}/{max_qa}",
                                    callback_data=cf.new(id=f"'qa'.{offset}", action="qa_view_text"))

    keyboard.add(but_back, but_text, but_next)
    return keyboard


def inline_for_view_categories():
    keyboard = InlineKeyboardMarkup()

    but_last_view = InlineKeyboardButton("◾️ Останні переглянуті", callback_data=cf.new(id=f"last_view", action="categories_view"))
    but_popular_view = InlineKeyboardButton("▫️ Популярні по перегляду", callback_data=cf.new(id=f"popular_view", action="categories_view"))
    but_max_comment = InlineKeyboardButton("◾️ Популярні по відгукам", callback_data=cf.new(id=f"max_comment", action="categories_view"))
    

    keyboard.add(but_last_view)
    keyboard.add(but_popular_view)
    keyboard.add(but_max_comment)
    return keyboard


def inline_for_view_category(data, icon):
    keyboard = InlineKeyboardMarkup()

    for i in range(0, len(data), 2):
        but = InlineKeyboardButton(f"{data[i][0]}   ({data[i][1]}{icon})", callback_data=cf.new(id=f"{data[i][0]}", action="number_view"))
        if i+1 < len(data):
            but1 = InlineKeyboardButton(f"{data[i+1][0]}   ({data[i+1][1]}{icon})", callback_data=cf.new(id=f"{data[i+1][0]}", action="number_view"))
            keyboard.add(but, but1)
        else:
            keyboard.add(but)

    del_but = InlineKeyboardButton("❌", callback_data=cf.new(id=f"-", action="delete"))
    keyboard.add(del_but)
    return keyboard