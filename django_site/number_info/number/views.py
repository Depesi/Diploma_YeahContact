from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .helper import *
import datetime
from django.utils import timezone
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin


def handle_page_not_found(request, *args, **kwargs):
    return render(request, 'number/404.html')


def index(request):
    context = get_context()
    # print(context.__str__())
    return render(request, 'number/index2.html', context=context)


def search_form(request):
    phone_number = request.POST['number']
    print(phone_number)
    if phone_number is "":
        return redirect('index')
    phone_number = is_phone_number(number=phone_number)

    return redirect('search_number', phone_number)


def search(request, number):
    context = get_context()

    phone_number = number
    page = request.GET.get('page', 1)
    number_activity = Number.objects.raw(f'SELECT na.*, n.* FROM "number_activity" as na INNER JOIN "number" as n ON n.id=na.id_number WHERE n.number=%s', [phone_number])
    if number_activity:
        number_activity = number_activity[0]
        NumberModel = Number.objects.get(id=number_activity.id_number)
        if not request.GET.get('page'):
            n = NumberActivity.objects.get(id_number=number_activity.id_number)
            n.last_view_date = datetime.now(tz=timezone.get_current_timezone())
            n.views += 1
            n.save()
            dv = DateView.objects.filter(id_number=NumberModel, date=datetime.now(tz=timezone.get_current_timezone()).date())
            if dv:
                dv[0].views += 1
                dv[0].save()
            else:
                dv = DateView(id_number=NumberModel, date=datetime.now(tz=timezone.get_current_timezone()).date(), views=0)
                dv.save()
    else:
        number_id = Number(number=phone_number,
                           date_added=datetime.now(tz=timezone.get_current_timezone()),
                           is_active=True)
        number_id.save()
        number_activity = NumberActivity(id_number=number_id.id,
                                         last_view_date=datetime.now(tz=timezone.get_current_timezone()),
                                         views=1)
        number_activity.save()
        date_view = DateView(id_number=number_id, date=datetime.now(tz=timezone.get_current_timezone()).date(), views=0)
        date_view.save()

    NumberModel = Number.objects.filter(id=number_activity.id_number)[0]
    if NumberModel:
        comments = Comment.objects.filter(id_number=NumberModel)
        comments_count = len(comments)
    else:
        comments_count = 0
    if comments_count > 0:
        comments_last_add = comments[len(comments)-1].date_create
        comments_stat = get_comments_stat(comments)
    else:
        comments_last_add = None
        comments_stat = 0
    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context['number'] = number_activity
    context['comments'] = comments
    context['phone_number'] = phone_number

    context['comments_count'] = comments_count
    context['comments_last_add'] = comments_last_add
    context['comments_stat'] = comments_stat

    # stats
    stats_data = DateView.objects.filter(id_number=NumberModel).order_by('-date')[:5]
    stats_date = []
    stats_views = []
    for i in range(len(stats_data)-1, -1, -1):
        stats_date.append(str(stats_data[i].date.strftime("%d.%m.%Y")))
        stats_views.append(stats_data[i].views)
    context['stats_date'] = json.dumps(stats_date)
    context['stats_views'] = json.dumps(stats_views)

    return render(request, 'number/index2.html', context=context)


def send_comment(request, number):
    content = request.POST['comment']
    date_create = datetime.now()
    level_id = request.POST['btnradio']

    level = Levels.objects.get(id=level_id)
    id_number = Number.objects.get(number=number)

    comment = Comment(id_number=id_number, content=content, date_create=date_create, level=level)
    comment.save()

    comment_activty = CommentActivity(id_comment=comment.id, good=0, bad=0)
    comment_activty.save()

    return redirect('search_number', number)


def contacts(request):
    return render(request, 'number/contacts.html')


def contacts_submit(request):
    username = request.POST['username']
    email = request.POST['email']
    message = request.POST['message']
    create_at = datetime.now(tz=timezone.get_current_timezone())
    obj = Contacts(username=username, email=email, message=message, create_at=create_at, answered=False)
    obj.save()
    return redirect('contacts')


def questions(request):
    data = Questions.objects.all().order_by('index')

    return render(request, 'number/questions.html', context={'questions': data})


@login_required
def admin_index(request):
    return render(request, 'number/admin/index.html')


class QuestionView(LoginRequiredMixin, View):
    def get(self, request):
        form = QuestionForm()

        return render(request, 'number/admin/create_question.html', context={'form': form})

    def post(self, request):
        data = QuestionForm(request.POST)
        if data.is_valid():
            obj = Questions.objects.filter(index=request.POST['index'])
            if obj:
                obj = obj[0]
                obj.question = request.POST['question']
                obj.answer = request.POST['answer']
                obj.save()
            else:
                question = data.save()
            return redirect('admin_index')
        return render(request, 'number/admin/create_question.html', context={'form': data})


def admin_question_delete(request):
    id = request.POST['id']
    if id:
        obj = Questions.objects.get(id=id)
        obj.delete()
    return redirect('questions')


class ContactsView(LoginRequiredMixin, View):
    def get(self, request):
        data = Contacts.objects.filter(answered=False).order_by('id')
        return render(request, 'number/admin/view_contacts.html', context={'contacts': data})

    def post(self, request):
        id = request.POST['id']
        obj = Contacts.objects.filter(id=id)[0]
        if obj:
            obj.answered = True
            obj.save()
        return redirect('admin_contacts')
