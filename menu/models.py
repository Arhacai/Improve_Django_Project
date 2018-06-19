from django.db import models
from django.utils import timezone


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_day = models.DateField(default=timezone.now)
    expiration_day = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_day = models.DateField(default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        'Ingredient', related_name='ingredients')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
