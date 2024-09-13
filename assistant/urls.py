from django.urls import path
from . import views
urlpatterns = [
    path('message/<query>', views.assistant, name='assistant'),
    path('reset/', views.clear_session, name='reset_assistant')
]
