from django.db import models
from django.utils import timezone
from userprofile.models import Profile
import uuid

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comment_set.filter(approved_comment=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date', 'created_date']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.PROTECT)
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['approved_comment', '-created_date']
