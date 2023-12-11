from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False, blank=False)
    profile_image = models.ImageField(null=False, blank=False, upload_to="images/profile/")
    biography = models.TextField(null=False, blank=False)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class Post(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
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
