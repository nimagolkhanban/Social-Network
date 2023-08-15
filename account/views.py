from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth import authenticate,login,logout



class RegisterView(View):
    form_class = UserRegistrationForm


    def get(self, request):
        form = self.form_class()
        return render(request, "account/register.html" , {"form":form})



    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"] , cd["email"], cd["password1"])
            messages.success(request,"you register succesfully", "success")
            return redirect("home:home")
        else :
            return render(request, "account/register.html", {"form": form})




class LoginView(View):
    form_class = UserLoginForm


    def get(self, request):
        form = self.form_class()
        return render(request, "account/login.html" , {"form":form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd["username"],password=cd["password"])
            if user is not None:
                login(request,user)
                messages.success(request,"you loged in succesfully", "success")
                return redirect("home:home")
            messages.error(request, "username or password is wrong" , "warning")

        return render(request, "account/login.html", {"form": form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,"loges out seccussfully","success")
        return redirect("home:home")

