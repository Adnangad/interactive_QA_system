from . import views
from django.urls import path

urlpatterns = [
    path("history", views.chat_history, name="history"),
    path("prompt", views.prompt, name="prompt")
]