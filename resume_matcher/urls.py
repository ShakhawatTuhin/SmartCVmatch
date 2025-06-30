from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bookmark/', views.bookmark_job, name='bookmark_job'),
    path('unbookmark/', views.unbookmark_job, name='unbookmark_job'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/profile/'), name='password_change'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
