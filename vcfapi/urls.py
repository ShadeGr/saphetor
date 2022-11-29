from django.urls import path

from .views import VCFView

urlpatterns = [
    path('records/', VCFView.as_view()),
]