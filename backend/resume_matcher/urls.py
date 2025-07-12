from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from . import api

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', api.UserViewSet, basename='user')
router.register(r'resumes', api.ResumeViewSet, basename='resume')
router.register(r'bookmarks', api.BookmarkViewSet, basename='bookmark')
router.register(r'jobs', api.JobViewSet, basename='job')  # Register the new JobViewSet

# API URLs - these will be included under /api/
api_urlpatterns = [
    path('', api.api_root),  # Root API endpoint
    path('', include(router.urls)),
]

# Template URLs - these will be included at root
template_urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('bookmark-job/', views.bookmark_job, name='bookmark_job'),
    path('unbookmark-job/', views.unbookmark_job, name='unbookmark_job'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/profile/'), name='password_change'),
]

# Use api_urlpatterns when included under /api/, and template_urlpatterns when included at root
urlpatterns = api_urlpatterns + template_urlpatterns
