from django.contrib import admin

from django.contrib import admin
from .models import CustomUser, Movie, Review, Genre

admin.site.register(CustomUser)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)

