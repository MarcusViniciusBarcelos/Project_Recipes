from django.contrib import admin

from .models import Rules, Values, Variables


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description', 'variable__name',)
    list_per_page = 25


@admin.register(Values)
class ValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'variables')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25


@admin.register(Variables)
class VariablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'values__name')
    list_per_page = 25
