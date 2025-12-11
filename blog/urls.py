from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('authors', views.authors, name='authors'),
    path('category', views.category, name='category'),
    path('post', views.post, name='post'),
]