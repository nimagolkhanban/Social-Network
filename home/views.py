from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView

from .models import Post
from .forms import PostCreateUpdateForm

class HomeView(View):

    def get(self, request):
        post = Post.objects.all()
        return render(request,"home/index.html", {"posts":post})

    def post(self, request):
        return render(request,"home/index.html")


class PostDetailView(View):

    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, "home/detail.html", {"post": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "your post has been deleted", "success")
        else:
            messages.error(request, "this in not your post", "danger")
        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request, "this post is not yours so you can't edit it", "danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = PostCreateUpdateForm(instance=post)
        return render(request, "home/update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = PostCreateUpdateForm(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.save()
            messages.success(request, "your post has been changed", "success")
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostCreateUpdateForm()
        return render(request, "home/create.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = PostCreateUpdateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "you create a post", "success")
            return redirect('home:post_detail', new_post.id,new_post.slug)
        messages.error(request, "form is not valid ", "warning")
        return redirect('home:post_create')


