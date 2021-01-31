from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars

from PIL import Image

class RegistrationForm(UserCreationForm):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField( max_length=100)
    class Meta:
        ordering=('-pk',)

# Create your models here.
# class  user(models.Model):
#     username = models.CharField(max_length=100,min_length=6,unique=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100,unique=True)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='profile/images' ,verbose_name='profile_pic',max_length=200,default='profile/profile.jpg',blank=True)
    email_confirmed = models.BooleanField(default=False)
    class Meta:
        ordering=('-pk',)
        
        
    @property
    def short_description(self):
        return truncatechars(self.description,20)
    
    def post_images(self):
        return mark_safe('<img src="{}" width="100" hieght="100" />' .format(self.images.url))
    post_images.short_description='Profile picture'
    post_images.alow_tags=True
    
    
    
    def __str__(self):
        return f'{self.user.username} profile'
    
   
    
    def save(self):
        super().save()
        
        img=Image.open(self.images.path)
        if img.height>400 or img.width>400:
            output_size=(400,400)
            img.thumbnail(output_size)
            img.save(self.images.path)