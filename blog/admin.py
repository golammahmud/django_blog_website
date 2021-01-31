

# Register your models here.
from django.contrib import admin

from .models import Post,Contact,Category

from users.models import Profile


from django.contrib.auth.models import Group
# Register your models here.
admin.site.site_header='admin dashboard'
admin.site.site_title='welcome to admin dashboard'
admin.site.index_title='welcome to django blog dashboard'



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'slug',)
    
    
class PostAdmin(admin.ModelAdmin):
    # list_display=('blog_image','title', 'category','author','date_created')
    list_display=('title', 'category','author','date_created')
    list_filter=('title', 'category','author')
     
    list_editable=('author',)
    list_display_links=('title', 'category',)
    search_fields=('title', 'category','author',)
    # read_only_fields=('blog_image','date_created', )
    read_only_fields=('date_created', )
    fieldsets=((None,{
          'fields':(
               'title', 
               'slug',
               'category',
               'content',
               'author',
               'date_created',
               'p_image',
            #    'post_images'
          )
     }),
                )
     
     
     
admin.site.register(Post,PostAdmin)    
# admin.site.register(Post)



class UserProfileAdmin(admin.ModelAdmin):
     list_display=('post_images','user')
     list_filter=('user', )
    #  list_editable=('user', )
     list_display_links=('user', )
     list_display_links=('post_images','user',)
     search_fields=('user', )
     read_only_fields=('post_images' )
    #  fieldsets=((None,{
    #       'fields':(
    #            'title', 
    #            'slug',
    #            'category',
    #            'content',
    #            'author',
    #            'date_created',
    #            'image',
    #            'post_images'
    #       )
    #  }),
    #             )
     

admin.site.register(Profile,UserProfileAdmin)
admin.site.register(Contact)
