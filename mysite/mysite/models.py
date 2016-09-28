from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Genre(models.Model):
    """Genre model"""
    title = models.CharField(max_length=100)


class Publisher(models.Model):
    """Publisher"""
    title = models.CharField(max_length=100)
    prefix = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
class Author(models.Model):
    """Author"""
    user = models.ForeignKey(User, blank=True, null=True)
    profession = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    
class Book(models.Model):
    """Book model"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published = models.DateField(blank=True, null=True)
    
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    authors = models.ManyToManyField(Author)

    