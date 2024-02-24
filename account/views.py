from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Post
from django.urls import reverse, reverse_lazy
from .models import Relation
class UserRegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'you are already logged in')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password1"])
            messages.success(request, "you registered successfully","success")
            return redirect("home:home")
        return render(request, "account/register.html", {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"

    def setup(self, request, *args, **kwargs):
        self.next_page = request.GET.get("next")
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'you are already logged in')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "you login successfully", "success")
                if self.next_page:
                    return redirect(self.next_page)
                return redirect("home:home")
            messages.warning(request, "invalid username or password", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, "you have logged out successfully", "success")
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_follow = False
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_follow = True
        return render(request, "account/profile.html", {"user": user, "posts": posts, "is_follow": is_follow})


class UserPasswordResetView(PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "you cant follow yourself", "danger")
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, f"you followed {user}", "success")
        return redirect("account:user_profile", user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f"you unfollowed {user}", "success")
        else:
            messages.error(request, "you cant unfollow yourself", "danger")
        return redirect("account:user_profile", user.id)
