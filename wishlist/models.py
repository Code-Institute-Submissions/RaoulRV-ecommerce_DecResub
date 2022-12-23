from django.db import models
from django.contrib.auth.models import User
from products.models import Carlist


class Wishlist(models.Model):

    class Meta:
        verbose_name_plural = 'Wishlists'

    wishlist_cars = models.ManyToManyField(Carlist, blank=True)
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.user_name}'s Wishlist"
