
from django.urls import path

from .views import *

app_name = 'especialista'


urlpatterns = [
    path('questions/', QuestionsList.as_view(), name='questions-list'),
    path('rules/', RulesList.as_view(), name='rules-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('rules/<int:pk>/', RuleDetailView.as_view(), name='rule-detail'),
]
