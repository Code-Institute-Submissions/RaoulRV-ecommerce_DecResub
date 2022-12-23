from django.urls import path
from . import views


urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add_wishlist/<item_id>/',
         views.add_wishlist, name='add_wishlist'),
]
