from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('authors', views.authors, name='authors'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('post/<slug:slug>/', views.post, name='post'),
]