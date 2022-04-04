from __future__ import unicode_literals
from django.shortcuts import render
from django.http  import HttpResponse
import photoapp
from .forms import NewsLetterForm
from .email import send_welcome_email

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
import datetime as dt
from .models import Comment, NewsLetterRecipients, Photos, Profile
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
    
        return render(request, 'all-photoapp/profile.html',display)
    return HttpResponseRedirect(request.path_info) 

@login_required(login_url='/accounts/login/')
def newpost(request):
    current_user=request.user
    user_profile=Profile.objects.filter(user=current_user)
    if request.method=='POST':
        form = NewPost(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data.save()
            # title=form.cleaned_data.get('title')
            # image=form.cleaned_data.get('image')
            # captions=form.cleaned_data.get('post')
            # user=form.cleaned_data.get('user')
            # post = Photos(title=title, image=image, post=captions,user=user)
            # post.save()
        else:
            print(form.errors)
        
        return HttpResponseRedirect(request.path_info)
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
    if 'image' in request.GET and request.GET["image"]:
        search_term = request.GET.get("image")
        print(search_term)
        searched_results = Photos.search(search_term)
        message = f"{search_term}"

        return render(request, 'all-photoapp/search.html',{"message":message,"results": searched_results})

    else:
        print('Say Chesee')
        message = "You haven't searched for any term"
        return render(request, 'all-photoapp/search.html',{"message":message})

from .email import send_welcome_email
def newsletter(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('')
            #.................
    return render(request, 'all-photoapp/home.html', {"date": date,"photoapp":photoapp,"letterForm":form})

