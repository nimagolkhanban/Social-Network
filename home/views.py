from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts":posts})


class PostDetailViews(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id,slug=post_slug)
        print(request)
        return render(request ,"home/detail.html" , {"post": post})


class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id :
            post.delete()
            messages.success(request,"post deleted successfully","success")
        else:
            messages.error(request,"you cant delete this post","danger")
        return redirect("home:home")

