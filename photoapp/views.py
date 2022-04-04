from __future__ import unicode_literals
from django.shortcuts import render
from django.http  import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
import datetime as dt
from .models import Comment, Photos, Profile
from .forms import (CommentForm, CreateUserForm, NewPost, UserUpdate, ProfileForm)


# Create your views here.
# def welcome(request):
#     return HttpResponse('Welcome to Instagram')


def home(request):
    post=Photos.objects.all()
    editor=User.objects.all()
    date=dt.date.today()
    current_user = request.user
    return render(request, 'all-photoapp/home.html',{"post":post,"editor":editor,"date":date,"current_user":current_user})


def registrationPage(request):
    form=CreateUserForm()
    
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,"django_registration/registration_form.html",{"form":form})

@login_required(login_url='/accounts/login/')
def comment(request,id):
    comment=Comment.objects.filter(image=id)
    image=Photos.objects.filter(image=id).all()
    current_user=request.user
    image=get_object_or_404(Photos,id=id)
    if request.method=='POST':
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            comment=commentForm.save(commit=False)
            comment.image=image
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        commentForm=CommentForm()
    return render(request,'all-photoapp/comment.html',{"commentForm":commentForm,"comment":comment,"image":image})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    if request.method == 'POST':

        userForm = UserUpdate(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user)

        if  profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        profile_form = ProfileForm(instance=request.user)
        user_form = UserUpdate(instance=request.user)
    

        display = {
            'user_form':user_form,
            'profile_form': profile_form
        }

    return render(request, 'all-photoapp/profile.html', display)

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user=request.user
    user_profile=Profile.objects.filter(user=current_user)
    if request.method=='POST':
        form = NewPost(request.POST,request.FILES)
        if form.is_valid():
            title=form.cleaned_data.get('title')
            image=form.cleaned_data.get('image')
            captions=form.cleaned_data.get('post')
            user=form.cleaned_data.get('user')
            post = Photos(title=title, image=image, post=captions,user=user)
            post.save()
        else:
            print(form.errors)
        
        return redirect('home')
    else:
        form=NewPost()
    return render(request,'all-photoapp/post.html',{'form':form})

@login_required(login_url='/accounts/login/')
def details(request,image_id):
    try:
        image = Photos.objects.get(id=image_id)
    except DoesNotExist:
        raise Http404()
    return render(request, 'all-photoapp/details.html', {"image": image})

def search_results(request):
    
    if 'Photo' in request.GET and request.GET["Photo"]:
        search_term = request.GET.get("Photo")
        print(search_term)
        searched_results = Photos.search(search_term)
        message = f"{search_term}"

        return render(request, 'all-photoapp/search.html',{"message":message,"results": searched_results})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-photoapp/search.html',{"message":message})


