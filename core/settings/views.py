from django.shortcuts import render, redirect
from users.models import CustomUser as User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from PIL import Image


def profil_settings(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    one_user = User.objects.get(pk = request.user.id)
    
    if one_user != request.user:
        return redirect(f"/user_profile")
    
    
    if request.method == "POST":
        user_img = request.FILES.get("user_img")
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        bio = request.POST.get("bio")

        if user_img and user_img != one_user.avatar:
            try:
                img = Image.open(user_img)
                img.verify()  
            except:
                return redirect(f"settings/")

            one_user.avatar = user_img
            
        if username and username != one_user.username:
            if len(username) < 30 and  not(username in User.objects.values_list('username', flat=True)):
                one_user.username = username
                
        if email and email != one_user.email:
            validator = EmailValidator()
            try:
                validator(email) 
             
                one_user.email = email
            except ValidationError as e:
                pass

        if first_name and first_name != one_user.first_name:
            if len(first_name) < 50:
                one_user.first_name = first_name
            
        if last_name and last_name != one_user.last_name:
            if len(last_name) < 50:
                one_user.last_name = last_name
            
        if bio and bio != one_user.description:
            one_user.description = bio
                
        one_user.save()
        return redirect(f"/settings")
    
    return render(request, "settings/profil_settings.html", context = {
       "one_user":  one_user,
       "active": "profile"
    })
    
    

def confid_settings(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    one_user = User.objects.get(id = request.user.id)
    
    
    if request.method == "POST":
        avatar_visibility = request.POST.get("avatar_visibility")
        activity_visibility = request.POST.get("activity_visibility")
        show_likes = request.POST.get("show_likes")
        show_dislikes = request.POST.get("show_dislikes")
        show_favorites = request.POST.get("show_favorites")
         
         
        print(type(show_likes), show_dislikes, show_favorites)
        
        
        
        if show_likes == None:
            one_user.show_likes = False
        else:
            one_user.show_likes = True
            
        if show_dislikes == None:
            one_user.show_dislikes = False
        else:
            one_user.show_dislikes = True        
            
        if show_favorites == None:
            one_user.show_favorites = False
        else:
            one_user.show_favorites = True
            
        if avatar_visibility != one_user.avatar_visibility:
            one_user.avatar_visibility = avatar_visibility
            
        if activity_visibility != one_user.activity_visibility:
            one_user.activity_visibility = activity_visibility
            
        one_user.save()
        return redirect("confid_settings")
    
    return render(request, "settings/confid_settings.html", context = {
        "active": "confid",
        "one_user": one_user
    })