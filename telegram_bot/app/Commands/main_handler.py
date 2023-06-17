from aiogram import types
from babel.dates import format_datetime
import datetime
import math
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from app.Core import dp, bot
from app.Menu import inline_for_number
from app.Helper import number_with_character, is_phone_number
from app.Db.commands import select_number_info, update_number_activity, select_all_comments


def mashine_learning(number):
    try:

        alchemyEngine = create_engine(
            'postgresql+psycopg2://postgres:password@localhost:5455/phone_number')
        dbConnection = alchemyEngine.connect()

        pd.set_option('display.float_format', lambda x: '%.3f' % x)

        phones_df = pd.read_sql('SELECT id, number FROM number;', dbConnection)

        phones_df.isnull().sum()

        comments_df = pd.read_sql_query(
            'select id as comment_id, id_number, level, level as lll from comment;', dbConnection, dtype={"id_number": 'int32', "level": 'float32'})

        comments_df.isnull().sum()

        phones_merged_df = phones_df.merge(
            comments_df, left_on='id', right_on="id_number")

        phones_merged_df = phones_merged_df.dropna(axis=0, subset=['id'])

        phones_average_rating = phones_merged_df.groupby('id')['level'].mean().sort_values(
            ascending=False).reset_index().rename(columns={'level': 'Average Rating'})

        phones_rating_count = phones_merged_df.groupby('id')['level'].count().sort_values(
            ascending=True).reset_index().rename(columns={'level': 'Rating Count'})  # ascending=False
        phones_rating_count_avg = phones_rating_count.merge(
            phones_average_rating, on='id')

        rating_with_RatingCount = phones_merged_df.merge(
            phones_rating_count, left_on='id', right_on='id', how='left')

        popularity_threshold = 1

        popular_phones = rating_with_RatingCount[rating_with_RatingCount['Rating Count']
                                                 >= popularity_threshold]

        phones_features_df = popular_phones.pivot_table(
            index='number', columns="lll", values='level').fillna(0)

        print(phones_features_df)
        phones_features_df_matrix = csr_matrix(phones_features_df.values)

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(phones_features_df_matrix)

        distances, indices = model_knn.kneighbors(
            phones_features_df.loc[number].values.reshape(1, -1), n_neighbors=4)

        recommended_phones = ""

        print(phones_features_df.loc[number].values)

        for i in range(0, len(distances.flatten())):
            if i == 0:
                print('Recommendations for {0}:\n'.format(number))
            else:
                if phones_features_df.index[indices.flatten()[i]] == number:
                    continue
                else:
                    recommended_phones += " \\" + \
                        phones_features_df.index[indices.flatten()[i]]
                    print('{0}: {1}, with distance of {2}:'.format(
                        i, phones_features_df.index[indices.flatten()[i]], distances.flatten()[i]))

        return recommended_phones
    except:
        return ""


def get_number_info(number):
    data = select_number_info(number)
    update_number_activity(data[0])
    comments_stats = get_comments_stat(select_all_comments(data[0]))
    rating = ""
    for i in range(0, 100, 10):
        if i < comments_stats:
            rating += "🔴"
        else:
            rating += "🟢"
    result = f"`Номер телефону:` {number_with_character(data[1])}\n\n" \
        f"`Рейтинг:` {rating}\n" \
        f"`Дата останнього перегляду:`  _{format_datetime(data[2], 'd MMMM Y', locale='uk_UA')}_\n" \
        f"`Кількість переглядів:`  _{data[3]}_"
    keyboard = inline_for_number(f"", data[0])
    return result, keyboard


@dp.message_handler(content_types=['text'])
async def main_text_handler(message: types.Message):
    isPhone, number = is_phone_number(message.text)
    if isPhone:
        data = select_number_info(number)
        recommended = mashine_learning(number)
        update_number_activity(data[0])
        comments_stats = get_comments_stat(select_all_comments(data[0]))
        rating = ""
        for i in range(0, 100, 10):
            if i < comments_stats:
                rating += "🔴"
            else:
                rating += "🟢"
        result = f"`Номер телефону:` {number_with_character(data[1])}\n\n" \
                 f"`Рейтинг:` {rating}\n" \
                 f"`Дата останнього перегляду:`  _{format_datetime(data[2], 'd MMMM Y', locale='uk_UA')}_\n" \
                 f"`Кількість переглядів:`  _{data[3]}_"

        if len(recommended) > 0:
            result += "\n`Можливо ви шукали? `" + recommended

        keyboard = inline_for_number(
            f"http://127.0.0.1:8000/search/{number}", data[0])
        await message.answer(result, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN_V2)
    else:
        await message.answer("Номер телефону введено не коректно😞")


def get_comments_stat(comments):
    if len(comments) == 0:
        return 0
    comments_stat = 0
    levels = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }
    for val in comments:
        levels[val[3].__str__()] += 1
    comments_stat = levels['1'] + levels['2']
    comments_stat = math.ceil(comments_stat * 100 / len(comments))
    return comments_stat
