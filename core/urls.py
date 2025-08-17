from django.urls import path
from . import views
from .views import register_view, verify_otp_view, login_view, logout_view, create_post_view, toggle_like_view, user_profile_view, edit_profile, toggle_follow, search_users_view, comments_view, delete_post, messages_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', register_view, name='register'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', create_post_view, name='create_post'),
    path('like/<int:post_id>/', toggle_like_view, name='toggle_like'),
    path('u/<str:username>/', user_profile_view, name='user-profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('toggle_follow/<str:username>/', toggle_follow, name='toggle_follow'),
    path('search/', search_users_view, name='search-users'),
    path('comments/<int:post_id>/', comments_view, name ='comments'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('messages/', messages_view, name='messages')
]