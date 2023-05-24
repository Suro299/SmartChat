from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from users.models import CustomUser as User
from PIL import Image
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


from .forms import NewUserForm, NewPostModelForm, NewComment
from .models import PostsModel, Tag, Comment


def posts(request):
    if not (request.user.is_authenticated):
        return redirect("login")

    if request.method == "POST":
        if not (request.user.is_authenticated):
            return redirect("login")
        
        btn_l = request.POST.get("btn_l")
        btn_d = request.POST.get("btn_d")
        btn_f = request.POST.get("btn_f")
        user = User.objects.get(username=request.user.username)
        
        if btn_l:
            prod = PostsModel.objects.get(id=btn_l)
            post_sender = User.objects.get(id = prod.sender.id)
            
            if request.user in prod.likers.all():
                prod.likers.remove(request.user)
                post_sender.exp -= 1
            else:
                prod.likers.add(request.user)
                post_sender.exp += 1
                
                if request.user in prod.dislikers.all():
                    prod.dislikers.remove(request.user)
            post_sender.save()
                
        elif btn_d:
            prod = PostsModel.objects.get(id=btn_d)
            if request.user in prod.dislikers.all():
                prod.dislikers.remove(request.user)
                
            else:
                prod.dislikers.add(request.user)

                if request.user in prod.likers.all():
                    prod.likers.remove(request.user)

        elif btn_f:
            prod = PostsModel.objects.get(id=btn_f)

            if prod in user.favorites.all():
                user.favorites.remove(prod)
                
            else:
                user.favorites.add(prod)
        try: 
            prod = PostsModel.objects.get(id = btn_l if btn_l else btn_d)
            post_sender = User.objects.get(id = prod.sender.id)

            if post_sender.exp >= 100:
                post_sender.exp -= 100
                post_sender.level += 1
            post_sender.save()
        except:
            pass
        
        prod.save()
        user.save()
    

    posts_list = PostsModel.objects.all()[::-1]

    return render(
        request,
        "main/posts.html",
        context={
            "posts_list": posts_list,
        },
    )


def about_us(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    return render(request, "main/about_us.html")




def confid_settings(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    return render(request, "main/confid_settings.html")


def confirm_delete(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    post = PostsModel.objects.get(pk=id)
    
    if request.user == post.sender:
        if request.method == "POST":
            post.delete()
            return redirect("posts")

        return render(request, "main/confirm_delete.html", context = {
            "post": post
        })
        
    return redirect(f"/post_page/{id}")

        
        


def create_post(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    message = ""
    if request.method == "POST":
        post_tags = request.POST.get("post_tags")
        post_title = request.POST.get("post_title")
        post_text = request.POST.get("post_text")

        if post_title:
            if len(post_title) > 100:
                return render(
                    request,
                    "main/create_post.html",
                    context={"message": "Title is too long"},
                )
        else:
            return render(
                request,
                "main/create_post.html",
                context={"message": "Please enter Title"},
            )

        if not (post_text):
            return render(
                request,
                "main/create_post.html",
                context={"message": "Please enter post text"},
            )

        form = NewPostModelForm(request.POST, request.FILES)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            if post_tags:
                tags = post_tags.split(" ")

                for i in tags:
                    if i and i != "#" and i[0] == "#":
                        if len(i) > 17:
                            return render(
                                request,
                                "main/create_post.html",
                                context={
                                    "form": form,
                                    "message": "Tag Error: Maximum tag length 15 characters",
                                },
                            )

                for i in tags:
                    i = i.strip()
                    if i != "" and i != "#" and i[0] == "#":
                        tag_instance, _ = Tag.objects.get_or_create(name=i[1:])
                        message.post_tags.add(tag_instance)

            user = User.objects.get(username=request.user.username)
            user.posts_posted += 1
            user.exp += 4

            if user.exp >= 100:
                user.exp -= 100
                user.level += 1

            user.save()

            return redirect("posts")
        else:
            print("!!! Post Creation Validation !!! ")
    else:
        form = NewPostModelForm()

    return render(
        request, "main/create_post.html", context={"form": form, "message": message}
    )


def lastest_update(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    return render(request, "main/lastest_update.html")


def post_page(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    post = PostsModel.objects.get(pk=id)

    if request.method == "POST":
        if not (request.user.is_authenticated):
            return redirect("login")
        
        btn_l = request.POST.get("btn_l")
        btn_d = request.POST.get("btn_d")
        post_comment = request.POST.get("post_comment")
        com_del = request.POST.get("com_del")
        
        if btn_l:
            comment_ex = Comment.objects.get(id=btn_l)
            sender = User.objects.get(id=comment_ex.com_sender.id)
            user = User.objects.get(id=request.user.id)

            if request.user in comment_ex.likers.all():
                comment_ex.likers.remove(request.user)
                if sender.points != 0 and sender.id != request.user.id:
                    sender.points -= 1
                    user.reactions -= 1

            else:
                if request.user in comment_ex.dislikers.all():
                    comment_ex.dislikers.remove(request.user)
                    
                comment_ex.likers.add(request.user)
                
                    

                if sender.id != request.user.id:
                    sender.exp += 2
                    sender.points += 1
                    user.reactions += 1

                if request.user in comment_ex.dislikers.all():
                    if sender.id != request.user.id:
                        comment_ex.dislikers.remove(request.user)
                        sender.points -= 1
                        user.reactions -= 1

            if sender.exp >= 100:
                sender.exp -= 100
                sender.level += 1
                
            sender.save()
            user.save()

            return redirect(f"/post_page/{id}")

        elif btn_d:
            comment_ex = Comment.objects.get(id=btn_d)
            sender = User.objects.get(id=comment_ex.com_sender.id)
            user = User.objects.get(id=request.user.id)

            if request.user in comment_ex.dislikers.all():
                comment_ex.dislikers.remove(request.user)
                if sender.points != 0 and sender.id != request.user.id:
                    sender.points -= 1
                    user.reactions -= 1

            else:
                if request.user in comment_ex.likers.all():
                    comment_ex.likers.remove(request.user)
                    
                comment_ex.dislikers.add(request.user)

                if sender.id != request.user.id:
                    sender.points += 1
                    sender.exp += 1
                    user.reactions += 1

                if request.user in comment_ex.likers.all():
                    if sender.id != request.user.id:
                        comment_ex.likers.remove(request.user)
                        sender.points -= 1
                        user.reactions -= 1
                        
            if sender.exp >= 100:
                sender.exp -= 100
                sender.level += 1
                

            sender.save()
            user.save()

        elif post_comment:
            form = NewComment(request.POST)

            if form.is_valid():
                
                comment = form.save(commit=False)
                comment.com_sender = request.user
                comment.save()
                post.comments.add(comment)
                sender = User.objects.get(id = post.sender.id)
                
                sender.exp += 4
                if sender.exp >= 100:
                    sender.exp -= 100
                    sender.level += 1
                
                sender.save()
        elif com_del:
            comment = Comment.objects.get(id = com_del)
            if comment.com_sender == request.user:
                comment.delete()

    else:
        form = NewComment()
        
    comments = list(post.comments.all())
    comments.reverse()

    return render(
        request, "main/post_page.html", context={
            "post": post, 
            "comments": comments
            }
    )


def profil_settings(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    one_user = User.objects.get(pk = id)
    
    if one_user != request.user:
        return redirect(f"/user_profile/{id}")
    
    
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
                return redirect(f"/profile_settings/{id}")

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
        return redirect(f"/profil_settings/{id}")
    return render(request, "main/profil_settings.html", context = {
       "one_user":  one_user
    })


def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        user_email = request.POST.get("email")

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email id"
            message = render_to_string(
                "main/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")

            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email],
                from_email="SmartChat <your_email@example.com>",  # указываете имя и email отправителя
            )

            email.content_subtype = "html"
            email.send()

            return render(
                request, "main/pls_check_email.html", context={"user_email": user_email}
            )
    else:
        form = NewUserForm()

    return render(request, "main/register.html", {"form": form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "main/verif_email.html")
    else:
        return render(request, "main/invalid_link.html")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("posts")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="main/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("posts")


def user_more(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    return render(request, "main/user_more.html")


def user_profile(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    one_user = User.objects.get(pk=id)
    next_level = one_user.level + 1

    last_posts = PostsModel.objects.filter(sender=one_user)[::-1]
    last_posts = last_posts[:4:]

    if request.method == "POST":
        follow = request.POST.get("follow")
        unfollow = request.POST.get("unfollow")
        send_message = request.POST.get("send_message")
        user = User.objects.get(id=request.user.id)
        edit_profile = request.POST.get("edit_profile")
        
        if follow:
            print("asd")
            one_user.subscribers_set.add(request.user)
            user.subscription_set.add(one_user)
            one_user.exp += 10

            if (user in one_user.subscribers_set.all()) and (one_user in user.subscribers_set.all()):
                user.friends_set.add(one_user)
                one_user.friends_set.add(user)

        elif unfollow:
            one_user.exp -= 10
            if (user in one_user.subscribers_set.all()) and (one_user in user.subscribers_set.all()):
                user.friends_set.remove(one_user)
                one_user.friends_set.remove(user)

            one_user.subscribers_set.remove(request.user)
            user.subscription_set.remove(one_user)
            
        elif edit_profile:
            if one_user == request.user:
                return redirect(f"/profil_settings/{id}")
        
        
        
        if one_user.exp >= 100:
            one_user.exp -= 100
            one_user.level += 1
            
        one_user.save()
        return redirect(f"/user_profile/{id}")

    return render(
        request,
        "main/user_profile.html",
        context={
            "one_user": one_user,
            "next_level": next_level,
            "last_posts": last_posts,
        },
    )


def verif_email(request):
    return render(request, "main/verif_email.html")


def pls_check_email(request):
    return render(request, "main/pls_check_email.html")


def invalid_link(request):
    return render(request, "main/invalid_link.html")


def ftf(request):
    return render(request, "main/404.html")
