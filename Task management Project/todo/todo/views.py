from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import TODOO
from django.contrib import messages

def home(request):
    # show a welcome / home. If user logged in redirect to todopage
    if request.user.is_authenticated:
        return redirect('todopage')
    return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm', '').strip()
        emailid = request.POST.get('emailid', '').strip()
        pwd = request.POST.get('pwd', '').strip()

        if not fnm or not emailid or not pwd:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        if User.objects.filter(username=fnm).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        User.objects.create_user(username=fnm, email=emailid, password=pwd)
        messages.success(request, "Account created. Please login.")
        return redirect('loginn')

    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm', '').strip()
        pwd = request.POST.get('pwd', '').strip()

        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('todopage')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('loginn')

    return render(request, 'loginn.html')

@login_required(login_url='/loginn/')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, "Please enter a task.")
            return redirect('todopage')

        TODOO.objects.create(title=title, user=request.user)
        return redirect('todopage')

    res = TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

@login_required(login_url='/loginn/')
def delete_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)
    obj.delete()
    messages.success(request, "Task deleted.")
    return redirect('todopage')

@login_required(login_url='/loginn/')
def edit_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            obj.title = title
            obj.save()
            messages.success(request, "Task updated.")
            return redirect('todopage')
        else:
            messages.error(request, "Title cannot be empty.")
    return render(request, 'edit_todo.html', {'obj': obj})

def signout(request):
    logout(request)
    return redirect('loginn')
