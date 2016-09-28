# myapp/api.py
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from tastypie import fields

# import the SpecificFieldsResource class
from specificfieldsresource import SpecificFieldsResource

# import the models
from models import *

class GenreResource(SpecificFieldsResource):
    class Meta:
        queryset = Genre.objects.all()
        resource_name = 'genre'
        include_resource_uri = False
        
class UserResource(SpecificFieldsResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['is_active', 'is_staff', 'is_superuser', 'password']
        include_resource_uri = False
        
class PublisherResource(SpecificFieldsResource):
    user = fields.ForeignKey(UserResource, 'user',  null=True, blank=True, full=True)

    class Meta:
        queryset = Publisher.objects.all()
        resource_name = 'publisher'
        include_resource_uri = False
        
class AuthorResource(SpecificFieldsResource):
    user = fields.ForeignKey(UserResource, 'user',  null=True, blank=True, full=True)
    
    class Meta:
        queryset = Author.objects.all()
        resource_name = 'author'
        include_resource_uri = False
        
class BookResource(SpecificFieldsResource):
    publisher = fields.ForeignKey(PublisherResource, 'publisher',  null=True, blank=True, full=True)
    genres = fields.ManyToManyField(GenreResource, 'genres', blank=True, full=True)
    authors = fields.ManyToManyField(AuthorResource, 'authors', full=True)

    class Meta:
        queryset = Book.objects.all()
        resource_name = 'book'
        include_resource_uri = False
        