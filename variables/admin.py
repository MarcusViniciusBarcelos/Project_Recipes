from django.contrib import admin

from .models import Questions, Rules


class QuestionsInline(admin.TabularInline):
    model = Rules.questions.through


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answer')
    list_display_links = ('id', 'title')
    list_per_page = 25


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'result')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'questions__title')
    list_filter = ('questions',)
    list_per_page = 25
    inlines = [QuestionsInline]
