from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('plan/<int:plan_id>/', views.plan_detail, name='plan-detail'),
    path('plan/<int:plan_id>/edit/', views.edit_plan, name='edit-plan'),
    path('plan/<int:plan_id>/delete/', views.delete_plan, name='delete-plan'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-plan/', views.create_plan, name='create-plan'),
    path('create-event/<int:plan_id>/', views.create_event, name='create-event'),
    path('home/', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)