from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import forms
from django.urls import reverse
# Create your models here.
# from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,default='')
    slug = models.SlugField(max_length=200, unique=True,default="No-Slug")

    class Meta:
     ordering = ('name',)
     verbose_name = 'category'
     verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
     return reverse('category-home-view',args=[self.slug])


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True)
    content = models.TextField(verbose_name='content')
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # post_photos=models.ImageField(blank=True,upload_to='blog/images' ,verbose_name='images',max_length=200)
    p_image=models.ImageField(blank=True,verbose_name='images',max_length=200,upload_to='blog/images',null=True)#,default='blog/post.jpg'
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk,'slug':self.slug})
    # @property
    # def short_description(self):
    #     return truncatechars(self.description,20)
    
    # def blog_image(self):
    #     return mark_safe('<img src="{}" width="100" hieght="100" />' .format(self.p_image.url))
    # blog_image.short_description='post_image'
    # blog_image.alow_tags=True
    class Meta:
        ordering = ('-date_created',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.title
    

class Contact(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()
    msg=models.TextField(verbose_name='message')
    
    class Meta:
        ordering = ('-pk',)
    
    def __str__(self):
        return  self.firstname + self.lastname
    