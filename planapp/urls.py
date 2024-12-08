from django.urls import path

from . import views
from .views import SignupView, SigninView, PlanView, add_view

urlpatterns  = [
    path('sign-up/', SignupView.as_view(), name='sign_up'),
    path('sign-in/', SigninView.as_view(), name='sign_in'),
    path('study-plan/', PlanView.as_view(), name='studyplan'),
    path('events/', add_view, name='add_event'),

]