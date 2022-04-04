from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField



# Create your models here.
class Profile(models.Model):
    profilephoto = CloudinaryField('image')
    Bio = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    following = models.ManyToManyField(User, blank=True, related_name='follow')

    def __str__(self):
        return self.Bio

    def delete_profile(self):
        self.delete()

    def save_profile(self):
        self.save()
    
    def update_profile(self):
        self.save()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

class Photos(models.Model):
    image = CloudinaryField('image')
    title = models.CharField(max_length=60)
    user = models.ForeignKey(User, blank=True,on_delete=models.CASCADE, null=True)
    caption= models.TextField(max_length=100)
    post = models.TextField(max_length=800)
    comments= models.IntegerField(default=150)
    pub_date = models.DateTimeField(auto_now_add=True,null=True)
    likes = models.ManyToManyField(User, related_name='post_like',default=None,blank=True)
    likes_counter=models.IntegerField(default=0)
    

    def __str__(self):
        return str(self.post)[:10]

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_caption(self,caption):
        self.caption = caption
        self.save()

    def number_of_likes(self):
        return self.likes.count()

    @classmethod
    def search(cls,search_term):
        photos=cls.objects.filter(title__icontains=search_term)
        return photos

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Photos, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True, null=True)

    def save_comment(self):
        self.save()

    def delete(self):
        self.delete()

class tags(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
        
class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
