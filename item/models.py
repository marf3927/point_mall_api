from django.db import models
from user.models import User
import random


class Category(models.Model):
    title = models.CharField(max_length=100)


class Tag(models.Model):
    tag = models.CharField(max_length=10)


def get_item_image_path(instance, filename):
    filename = str(random.randint(10000,100000)) + filename
    path = 'item_images/%s' % filename


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='items')
    tag = models.ManyToManyField(Tag, related_name='item')

    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='item_images/')


class UserItem(models.Model):
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


class History(models.Model):
    user = models.ForeignKey(User, related_name='histories', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_refunded = models.BooleanField(default=False)


class HistoryItem(models.Model):
    history = models.ForeignKey(History, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
