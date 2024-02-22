from django.shortcuts import render
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
