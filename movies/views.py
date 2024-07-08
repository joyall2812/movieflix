# movies/views.py
from django.db.models import Q
from django.shortcuts import render, redirect , get_object_or_404
from .forms import CustomUserCreationForm
from .forms import MovieForm
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Movie
from .models import Review
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import logging
import traceback


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print(f"User '{username}' authenticated successfully.")
                return redirect('user_page')  # Redirect to user page after login
            else:
                print(f"Authentication failed for user '{username}'.")
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# views.py



logger = logging.getLogger(__name__)

def search_view(request):
    query = request.GET.get('query', '').strip()
    logger.debug(f"Received query: '{query}'")
    
    if query:
        try:
            movies = Movie.objects.filter(title__icontains=query)
            logger.debug(f"Movies found: {movies}")
        except Exception as e:
            logger.error(f"Error filtering movies: {e}")
            logger.error(traceback.format_exc())
            movies = Movie.objects.none()
    else:
        movies = Movie.objects.none()
        logger.debug("No query provided, returning no movies.")
    
    return render(request, 'search_results.html', {'movies': movies})



def home(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie)  # Access reviews through related_name 'reviews'
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def user_page(request):
    user_movies = Movie.objects.filter(added_by=request.user)
    return render(request, 'user_page.html', {'user_movies': user_movies})


@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('user_page')
        else:
            print(form.errors)
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'movie': movie})

def movies_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genre=genre)
    return render(request, 'movies_by_genre.html', {'genre': genre, 'movies': movies})

def search_movies(request):
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'movies': movies, 'query': query})


