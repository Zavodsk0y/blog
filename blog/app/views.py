from django.urls import reverse_lazy
from django.views import generic

from .forms import *


class CreateProfileView(generic.CreateView):
    model = Profile
    template_name = 'create_profile.html'
    success_url = reverse_lazy('profile')
    form_class = CreateProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'profile.html'


class CreatePostView(generic.CreateView):
    model = Post
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    form_class = CreatePostForm


class PostsListView(generic.ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


class CreateCommentView(generic.CreateView):
    model = Comment
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    form_class = CreateCommentForm
