from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment,Photos

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email','password1','password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Bio','profilephoto']
        widgets = {
            'Bio': Textarea(attrs={'cols': 30, 'rows': 3}),
        }

class UserUpdate(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class NewPost(forms.ModelForm):
    class Meta:
        model = Photos
        exclude = ['pub_date', 'likes']


class CommentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] ='Add a comment...'
        
    class Meta:
        model=Comment
        fields = ('comment',)\

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')
 
        
       