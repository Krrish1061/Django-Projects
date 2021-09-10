from django.contrib import admin
from django.db.models.signals import post_save
from .models import Post

# Register your models here.
admin.site.register(Post)
