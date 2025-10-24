from django.contrib import admin
from main.models import Article, Events, Venue
# Register your models here.
admin.site.register(Article)
admin.site.register(Events)
admin.site.register(Venue)