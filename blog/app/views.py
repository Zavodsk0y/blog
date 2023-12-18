from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseForbidden, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import *


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Вы успешно вышли из аккаунта')
        return HttpResponseRedirect(reverse('login'))


class BBLoginView(LoginView):
    template_name = 'registration/login.html'


class CreateProfileView(LoginRequiredMixin, generic.CreateView):
    model = Profile
    template_name = 'create_profile.html'
    form_class = CreateProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_profile = user.profile
        context['user_profile'] = user_profile
        return context

    def form_valid(self, form):
        if not hasattr(self.request.user, 'profile'):
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return render(self.request, 'profile_already_exists.html')

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.profile.pk})


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = CreateProfileForm

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.profile.pk})


class DeleteProfileView(LoginRequiredMixin, generic.DeleteView):
    model = Profile
    template_name = 'delete_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('posts')


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context["posts"] = Post.objects.filter(user=user)
        post_comments = Comment.objects.filter(post__user=user)
        context["post_comments"] = post_comments
        context["comment_form"] = CreateCommentForm()
        profile = self.get_object()

        if self.request.user.is_authenticated and self.request.user == user:
            # Проверка, является ли текущий пользователь владельцем профиля
            context["create_post_form"] = CreatePostForm()
        else:
            context["create_post_form"] = None

        return context


class CreatePostView(generic.CreateView):
    model = Post
    template_name = 'profile.html'
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.profile.pk})


class PostsListView(generic.ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 50


class CreateCommentView(generic.CreateView):
    model = Comment
    template_name = 'profile.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        post_id = self.request.POST.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.profile.pk})


class EditCommentView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    template_name = 'edit_comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        post_id = self.object.post.id
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

        return response

    def get_success_url(self):
        post_id = self.object.post.id
        post = get_object_or_404(Post, pk=post_id)
        profile_pk = post.user.profile.pk
        return reverse('profile', kwargs={'pk': profile_pk})


class DeleteCommentView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'delete_comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this comment.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        profile_pk = self.object.post.user.profile.pk
        return reverse('profile', kwargs={'pk': profile_pk})
