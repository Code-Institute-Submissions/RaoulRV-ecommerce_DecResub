from django.contrib import admin
from .models import Carlist, Category, ReviewCar

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "priceperday",
        "rating",
        "image",
    )

    ordering = ("sku",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )


class CarReviewAdmin(admin.ModelAdmin):
    list_display = (
        'car',
        'user',
        'reviewtitle',
        'reviewtext',
        'status',
        'stars',
    )


admin.site.register(Carlist, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ReviewCar, CarReviewAdmin)
