from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("feedback", views.feedback_form_view, name="feedback"),
    path("contact", views.contact_us, name="contact"),
    path('about', views.about_us, name='about')
]
