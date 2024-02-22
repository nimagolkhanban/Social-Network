from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Post


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
