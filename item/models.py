from django.db import models

from user.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)

class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/item_images/')


class UserItem(models.Model):
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


