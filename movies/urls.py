from django.urls import path
from .views import movies, collection

urlpatterns = [
    path('movies/', movies.movies, name='movies'),
    path('collection/', collection.collection, name='collection'),
]