from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser
from django.contrib import auth


# Create your models here.

class Colleges(models.Model):
    name_college = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name_college


class User(models.Model):
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=50)

    # college = models.CharField(choices=COLLEGE_CHOICES)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name

    def set_password(self, password):
        pass


class Categories(models.Model):
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_desc = models.CharField(max_length=300, blank=True)

    # image
    def __str__(self):
        return self.name


class FoodItems(models.Model):
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    price = models.IntegerField(default=0)
    short_des = models.CharField(max_length=200, blank=True)

    # check for (on delete models.SET_NULL) IN CATEGORY TO AVOID DELETION OF MEALS
    # image

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    total = models.IntegerField()
    order_time = models.DateTimeField(default=timezone.now)
    pickup_time = models.TimeField(default=timezone.now)

    # qty
    # time
    # pickup time
    # order date
    # delivery status
    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    meal = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    # user
    def __str__(self):
        return str(self.id)


class Favourites(models.Model):
    meal = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_status = models.BooleanField()

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# settings.AUTH_USER_MODEL
