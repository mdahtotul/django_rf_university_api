from django.urls import path

from .views import *


urlpatterns = [
    path("que_bank/questions/", QuestionViewSet.as_view()),
]
