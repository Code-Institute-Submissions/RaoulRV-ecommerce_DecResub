from django.db import models

# Create your models here.


class ContactUs(models.Model):
    email_address = models.EmailField()
    name = models.CharField(
        max_length=100
        )
    message_subject = models.CharField(max_length=400)
    message = models.TextField()
    message_date = models.DateTimeField(
        auto_now_add=True
        )
    reply_sent = models.BooleanField(default=False)

    REGARDING_LIST = [
        ('breakdown assist', 'Breakdown assist'),
        ('refunds', 'Refunds'),
        ('vouchers', 'Vouchers'),
        ('rental duration', 'Rental duration'),
        ('pickup or dropoff', 'Pickup or dropoff'),
        ('cars', 'Cars'),
        ('other reason', 'Other reason'),

    ]
    regarding = models.CharField(
        max_length=24,
        choices=REGARDING_LIST,
        default='Select'
        )

    def __str__(self):
        return self.name
