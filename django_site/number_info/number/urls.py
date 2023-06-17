from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_form, name='search_form'),
    path('search/<str:number>/', views.search, name='search_number'),
    path('search/<str:number>/send', views.send_comment, name='send_comment'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/submit', views.contacts_submit, name='contacts_submit'),
    path('questions/', views.questions, name='questions'),

    path('admin/index', views.admin_index, name='admin_index'),
    path('admin/addQuestion', views.QuestionView.as_view(), name="admin_question"),
    path('admin/deleteQuestion', views.admin_question_delete, name="admin_question_delete"),
    path('admin/contacts', views.ContactsView.as_view(), name="admin_contacts"),

]
