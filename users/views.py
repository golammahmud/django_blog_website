from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from users.forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.
def register(request):
    if request.method == "POST":
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            messages.success(request, f'registration successully {username}')
            return redirect('home')
    else:
        form=UserRegistrationForm()
    return render(request,'users/registration.html',{'form':form})



@login_required(redirect_field_name='login')
def profile(request):
    if request.method == "POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'you have been updated')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
        
    return render(request,template_name='users/profile.html',context = {'u_form':u_form,'p_form':p_form}) 

@login_required(redirect_field_name='login')
def updateprofile(request):
    if request.method == "POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'you have been updated')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)   
    
    return render(request,template_name='users/updateprofile.html',context = {'u_form':u_form,'p_form':p_form})   

@login_required()
def logout(request):
    logout(request)
    return redirect('logout')