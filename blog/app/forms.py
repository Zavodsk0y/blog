from django import forms

from .models import *


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'biography', 'profile_image']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_image']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description', 'comment_image']