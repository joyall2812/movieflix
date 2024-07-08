from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/add_review/', views.add_review, name='add_review'),
    path('user_page/', views.user_page, name='user_page'),
    path('search/', views.search_view, name='search_movies'),
]
