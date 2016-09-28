from django.contrib import admin
from models import *

# Registering the models
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
