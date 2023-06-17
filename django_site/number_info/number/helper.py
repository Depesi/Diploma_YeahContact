from django.db.models import Max, Count
from .models import *
import phonenumbers
import math


def get_context():
    context = {}

    # last_view = NumberActivity.objects.order_by('-last_view_date')[:10]
    last_view = Number.objects.raw('SELECT na.*, n.* FROM "number_activity" as na INNER JOIN "number" as n ON n.id=na.id_number ORDER BY na.last_view_date DESC')[:10]
    popular_view = Number.objects.raw('SELECT na.*, n.* FROM "number_activity" as na INNER JOIN "number" as n ON n.id=na.id_number ORDER BY na.views DESC')[:10]
    popular_comments = Comment.objects.values('id_number__number').annotate(total=Count('id_number')).order_by('-total')[:10]
    context['last_view'] = last_view
    context['popular_view'] = popular_view
    context['popular_comments'] = popular_comments

    return context


def is_phone_number(number):
    v = None
    try:
        v = phonenumbers.parse(number, "UA")
        if v:
            if v.national_number < 9:
                return None
            else:
                phone_number = '+' + str(v.country_code) + str(v.national_number)
                return phone_number
    except phonenumbers.phonenumberutil.NumberParseException as ex:
        print(ex.__str__())
        return None


def get_comments_stat(comments):
    comments_stat = 0
    levels = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }
    for val in comments:
        levels[val.level.id.__str__()] += 1
    comments_stat = levels['1'] + levels['2']
    comments_stat = math.ceil(comments_stat * 100 / len(comments))
    return comments_stat
