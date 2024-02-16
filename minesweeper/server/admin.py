from django.contrib import admin

from .models import Game, Mine


class MineInline(admin.TabularInline):
    model = Mine
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [MineInline]
