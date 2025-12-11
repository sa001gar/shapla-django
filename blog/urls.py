from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('authors', views.authors, name='authors'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('category/<slug:category_slug>/<slug:post_slug>/', views.post, name='post'),
]