from django.contrib import admin
from .models import *

admin.site.register(Number)
# admin.site.register(NumberActivity)
admin.site.register(Comment)
# admin.site.register(CommentActivity)
admin.site.register(Levels)

