from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from  django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Post,Contact,Category
from users.forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin

from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView

from django.core.paginator import  Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import datetime

from blog.forms import ContactForm

from django.core.mail import send_mail,BadHeaderError
from django.conf import settings 

#decorators for functions based views and mixins for classed based views

# Create your views here.
def home(request):
    posts=Post.objects.filter(author=request.user).order_by('-pk')
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context={
        'posts':posts,
       
    }
    return render(request,template_name='blog/post.html',context={
        'posts':posts,
        
    })
    
def contact(request):
    form=ContactForm(request.POST)
    if form.is_valid():
            first_name=form.cleaned_data['firstname']
            last_name=form.cleaned_data['lastname']
            name=first_name +''+ last_name
            email=form.cleaned_data['email']
            message=form.cleaned_data['msg']
            form.save()
            if name and message and email:
                subject = f'Message From  django Block of {first_name}'
                message =  f'tthis message comes from {name}\n {message}\n {email}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['pranto.ahmed89@gmail.com' ] 
                try:
                    send_mail(subject,
                              message,
                              email_from, 
                              recipient_list,
                              fail_silently=False)
                    messages.success(request,f' Thanks {first_name} your message has been successfully sent!')
                    return redirect('contact')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('contact')
            else:
             return HttpResponse('Make sure all fields are entered and valid.')

            # send_mail(
            #     subject,#subject
            #     message,#message
            #     email_from,#from email
            #     recipient_list,#to email
                
            #     fail_silently=False
            # )
            # messages.success(request,f' Thanks {first_name} your message has been successfully sent!')
            # return redirect('contact')
    else:
        
        form=ContactForm()
        # messages.warning(request,'please fill in all fields properly!')
        
    
    return render(request,'blog/contact.html' ,{'form':form})


# def home(request):
    
#         posts: Post.objects.filter(author=request.user).order_by('-pk')
#         paginator = Paginator(posts, 25) # Show 25 contacts per page.

#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
    
#     return render(request, 'blog/home.html')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')
    
 
def PostListView(request,category_slug=None):
    category=None
    categories=Category.objects.all()
    
    if category_slug is not None:
        category=get_object_or_404(Category,slug=category_slug)
        posts=Post.objects.filter(category=category).order_by('-pk','date_created')
    else:
        posts=Post.objects.all().order_by('-pk','date_created')
    
    paginator = Paginator(posts, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request,template_name='blog/index.html',context = {"categories":categories,
                                                                     "category":category,
                                                                     "posts":posts,
                                                                     "page_obj":page_obj
        
    })
 
 
# class PostListView(ListView):
#     model=Post
#     template_name='blog/home2.html'
#     context_object_name='posts'
#     ordering=['-pk','date_created']
#     paginate_by=2
#     def get_queryset(self):
#         return super().get_queryset()
        
    
    
    
    
    
    
class PostDetailView(DetailView):
    model=Post
    template_name='blog/detail.html'
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug' # DetailView's default value: optional

class CreatePost(LoginRequiredMixin,CreateView):
    model=Post
    template_name='blog/create_post.html'
    fields=['title','slug','content','p_image']
    
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class UpdatePost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    template_name='blog/create_post.html'
    fields=['title','slug','content','p_image']
    
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
    
    
    
class DeletePost(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    template_name='blog/delete.html'
    success_url = '/post/'
   
    

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False


class AuthorListView(ListView):
    model=Post
    template_name='blog/post.html'
    context_object_name='posts'
    # ordering=['-pk']
    
    def get_queryset(self):
        # user = get_object_or_404(User, username=self.kwargs.get('pk'))
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')
    

def search(request):
  
    query=request.GET['query'][:50]
    authors=User.objects.filter(username__icontains=query)
    
    if len(query) >100:
       post=Post.objects.none()
    elif len(query ) < 1:
        post=Post.objects.none()
        messages.warning(request,'no search results found..please try again proper query')
        
    # if post.count()==0:
    #     messages.warning(request,'no search results found..please try again proper query')
    else:
        # post_title=Post.objects.filter(title__icontains=query)
        # post_content=Post.objects.filter(content__icontains=query)
        # post=post_title.union(post_content)
        post=Post.objects.filter(  Q( author__in=authors) |Q( title__icontains=query) | Q(content__icontains=query) |Q( pk__icontains=[query]) |Q(date_created__date__icontains=query) )
    # date_created
    context={
        'posts':post
    }
   
    return render(request,template_name='blog/search.html',context={
        'posts':post,'query':query,
    })