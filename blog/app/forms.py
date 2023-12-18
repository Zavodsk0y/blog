from django import forms

from .models import *


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'biography', 'profile_image']

    def clean_profile_image(self):
        # Получаем предоставленное изображение профиля
        profile_image = self.cleaned_data.get('profile_image')

        # Если изображение не предоставлено, устанавливаем дефолтное изображение
        if not profile_image:
            default_image_path = 'images/profile/default_picture.png'  # Замените на путь к вашему дефолтному изображению
            with open(default_image_path, 'rb') as default_image:
                profile_image = default_image

        return profile_image

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_image']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description', 'comment_image']