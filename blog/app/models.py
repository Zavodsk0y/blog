from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False, blank=False)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Post(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    post_image = models.ImageField(null=True, blank=True, upload_to='images/posts/')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    comment_image = models.ImageField(null=True, blank=True, upload_to='images/comments/')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
