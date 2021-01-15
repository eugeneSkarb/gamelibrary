from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('genres/<int:id>/', views.genre),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('add_game/', views.add_game, name='add_game'),
    path('create_game/', views.create_game),
    path('create_publisher/', views.create_publisher),
    path('create_game_studio/', views.create_game_studio),
    path('create_genre/', views.create_genre),
    path('games/<int:id>/', views.game),
    path('developers/<int:id>/', views.developer),
    path('rate_game/<int:id>/', views.rate_game),
    path('', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
