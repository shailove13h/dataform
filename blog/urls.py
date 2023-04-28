from django.urls import path

from . import views
from core.views import blog
from blog.views import post_like

urlpatterns = [
    path('post_like/<int:post_id>/', post_like, name='post_like'),
    path('search/', views.search, name='search'),
    path('blog/', blog, name='blog'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
    path('<slug:slug>/', views.category, name='category_detail')
]