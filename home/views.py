from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView

from .models import Post, Comment
from .forms import PostCreateUpdateForm, CommentCreateForm


class HomeView(View):

    def get(self, request):
        post = Post.objects.all()
        return render(request,"home/index.html", {"posts":post})

    def post(self, request):
        return render(request,"home/index.html")


class PostDetailView(View):
    comment_form = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs["post_id"], slug=kwargs["post_slug"])
        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = self.post_instance.pcomment.filter(is_reply=False)
        return render(request, "home/detail.html", {"post": self.post_instance, "comment": comment, "form": self.comment_form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.comment_form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "your comment submit", "success")
            return redirect(reverse("home:post_detail", args=(self.post_instance.id, self.post_instance.slug)))
class PostDeleteView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "your post has been deleted", "success")
        else:
            messages.error(request, "this in not your post", "danger")
        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs["post_id"])
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
            return redirect('home:post_detail', new_post.id, new_post.slug)
        messages.error(request, "form is not valid ", "warning")
        return redirect('home:post_create')


