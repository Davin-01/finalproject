from django.urls import path


from .views import SignupView, SigninView, PlanView

urlpatterns  = [
    path('sign-up/', SignupView.as_view(), name='sign_up'),
    path('sign-in/', SigninView.as_view(), name='sign_in'),
    path('plan/', PlanView.as_view(), name='plan'),
]