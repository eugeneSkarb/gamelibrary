from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .forms import GameForm
from .models import *


class GameAdmin(ModelAdmin):
    form = GameForm


# Register your models here.
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(GameStudio)
admin.site.register(Game, GameAdmin)
admin.site.register(UserRating)
admin.site.register(GameGenre)
