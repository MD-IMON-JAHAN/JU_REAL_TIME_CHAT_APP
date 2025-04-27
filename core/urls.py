from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-room/', views.create_room, name='create_room'),
    path('room/<uuid:room_id>/', views.room, name='room'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('rooms/<uuid:room_id>/invite/', views.invite_to_room, name='invite_to_room'),
]