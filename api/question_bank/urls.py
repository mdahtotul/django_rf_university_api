from django.urls import path

from .views import *


urlpatterns = [
    path("que_bank/questions/", QuestionViewSet.as_view()),
    path("que_bank/questions/<question_id>/", QuestionDetailsViewSet.as_view()),
    path("que_bank/questions/upload/", QuestionUploadViewSet.as_view()),
]
