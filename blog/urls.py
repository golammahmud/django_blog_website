from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import register,profile,updateprofile
from django.contrib.auth import views as auth_views
from blog.views import home,search,contact
from .views import PostListView,CreatePost,UpdatePost,DeletePost ,PostDetailView,UserPostListView

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    
    
    path('',PostListView, name='home'),
    path('<slug:category_slug>/',PostListView, name='category-home-view'),
    
    
    
    path('post/',home, name='post'),
    path('search/',search, name='search'),
    path('contact/',contact, name='contact'),
  
    
    path('blog/<int:pk>/<slug:slug>/', PostDetailView.as_view(),name='post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
   
    path('blog/new/', CreatePost.as_view(),name='create-post'),
    path('blog/<int:pk>/<slug:slug>/update', UpdatePost.as_view(),name='post-update'),
    path('blog/<int:pk>/<slug:slug>/delete', DeletePost.as_view(),name='post-delete'),
    path('register/', register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login' ),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/', profile,name='profile'),
    path('accoutupdate/', updateprofile,name='update-account'),

]