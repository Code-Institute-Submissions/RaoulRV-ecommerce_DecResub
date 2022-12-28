from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Carlist(models.Model):
    class Meta:
        verbose_name_plural = "Car List"

    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    priceperday = models.DecimalField(max_digits=15, decimal_places=0)
    horse_power = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=254, null=True, blank=True)
    msrp = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class ReviewCar(models.Model):
    class Meta:
        verbose_name_plural = "Car Reviews"

    car = models.ForeignKey(Carlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewtext = models.TextField(max_length=800, blank=True)
    reviewtitle = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stars = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=False)

    def __str__(self):
        return self.reviewtext
