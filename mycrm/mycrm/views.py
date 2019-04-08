from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
def access_login(request):
    errors = {}
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username = email,password = password)
        if user:
            login(request, user)
            next_url = request.GET.get("next","/")
            return redirect(next_url)
        else:
            errors['error'] = "*用户名或密码错误"
    return  render(request,"login.html",{"errors":errors})

def access_logout(request):
    logout(request)
    return redirect("/account/login/")

@login_required
def index(request):
    return  render(request,"newindex.html")

def newindex(request):
    return render(request,"newindex.html")