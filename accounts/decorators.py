from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render,redirect
def role_required(role_name):
    def check_role(user):
        return user.role.name == role_name if user.role else False
    return user_passes_test(check_role)

def signin_required(fn):
    def wrapper(request,*args,**kargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login to perform this action")
            return redirect("signin")
        return fn(request,*args,**kargs)
    return wrapper