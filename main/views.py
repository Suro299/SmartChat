import os
import shutil
import tempfile
from django.shortcuts import render, redirect
from users.models import CustomUser as User
from django.db.models import Q
from django.shortcuts import render
from .forms import  NewPostModelForm, NewComment
from .models import PostsModel, Tag, Comment
from io import BytesIO
import zipfile

from django.http import FileResponse
from django.shortcuts import render
from chat.models import Chat



def posts(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    unread_msg = get_unread_messages_count(request)
    
    upd_login(request)
    search_post = request.GET.get("search")
    posts_list = PostsModel.objects.all()
    user_list = []

    if search_post:
        search_post = search_post.strip()
        if search_post[0] == "$":
            posts_list = posts_list.filter(Q(id__icontains=search_post[1:]))
        elif search_post[0] == "@":
            posts_list = posts_list.filter(
                Q(sender__username__icontains=search_post[1:])
            )
        elif search_post[0] == "#":
            posts_list = posts_list.filter(
                Q(post_tags__name__icontains=search_post[1:])
            )
        elif search_post[:4].lower() == "all@":
            user_list = User.objects.filter(Q(username__icontains=search_post[4:]))
        else:
            posts_list = posts_list.filter(
                Q(post_title__icontains=search_post)
                | Q(post_text__icontains=search_post)
            )

        posts_list = posts_list[::-1]
    else:
        posts_list = PostsModel.objects.all()[::-1]

    if request.method == "POST":
        if not (request.user.is_authenticated):
            return redirect("login")
        reac(request)
        
    return render(
        request,
        "main/posts.html",
        context={
            "posts_list": posts_list,
            "test": User.objects.all(),
            "user_list": user_list,
            "total_unread_messages": unread_msg,
            "page": "posts"        
        },
    )


def confirm_delete(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    unread_msg = get_unread_messages_count(request)
    post = PostsModel.objects.get(pk=id)

    if request.user == post.sender or request.user.is_staff:
        if request.method == "POST":
            post.delete()
            return redirect("posts")

        return render(request, "main/confirm_delete.html", context={"post": post, "total_unread_messages": unread_msg,})

    return redirect(f"/post_page/{id}")


def create_post(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    unread_msg = get_unread_messages_count(request)
    
    message = ""
    if request.method == "POST":
        post_tags = request.POST.get("post_tags")
        post_title = request.POST.get("post_title")
        post_text = request.POST.get("post_text")

        if post_title:
            if len(post_title) > 100:
                return render(request, "main/create_post.html",
                    context={
                        "message": "Title is too long", 
                        "total_unread_messages": unread_msg,
                        }
                )
        else:
            return render(
                request,
                "main/create_post.html",
                context={
                    "message": "Please enter Title", 
                    "total_unread_messages": unread_msg,
                    }
            )

        if not (post_text):
            return render(
                request,
                "main/create_post.html",
                context={
                    "message": "Please enter post text", 
                    "total_unread_messages": unread_msg,
                    }
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
                                    "total_unread_messages": unread_msg,
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
        request, "main/create_post.html", context={
            "form": form, 
            "message": message, 
            "total_unread_messages": unread_msg,}
    )


def post_page(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    unread_msg = get_unread_messages_count(request)    
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
                    sender.exp += 1
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

            return redirect(f"/sc/post_page/{id}")

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
                sender = User.objects.get(id=post.sender.id)
                sender.exp += 4

                if sender.exp >= 100:
                    sender.exp -= 100
                    sender.level += 1

                sender.save()
        elif com_del:
            comment = Comment.objects.get(id=com_del)
            if comment.com_sender == request.user or request.user.is_staff:
                comment.delete()

    else:
        form = NewComment()

    comments = list(post.comments.all())
    comments.reverse()

    return render(
        request, "main/post_page.html", context={
            "post": post, 
            "comments": comments, 
            "total_unread_messages": unread_msg,
            }
    )




def user_more(request, act, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    unread_msg = get_unread_messages_count(request)
    user = User.objects.get(id=id)
    
    if act == "fov" and (user.show_favorites or request.user.is_staff or user.id == request.user.id):
        posts = user.favorites.all()[::-1]
    elif act == "likes" and (user.show_likes or request.user.is_staff or user.id == request.user.id):
        posts = PostsModel.objects.filter(likers = user)[::-1]
    elif act == "dislikes" and (user.show_dislikes or request.user.is_staff or user.id == request.user.id):
        posts = PostsModel.objects.filter(dislikers = user)[::-1]
    else:
        return redirect(f"/sc/user_profile/{user.id}")

   

    if request.method == "POST":
        reac(request)

    return render(request, "main/user_more.html", context={
        "posts": posts,
        "one_user": user,
        "total_unread_messages": unread_msg,
        })


def user_profile(request, id):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    unread_msg = get_unread_messages_count(request)
    one_user = User.objects.get(pk=id)
    next_level = one_user.level + 1

    user_posts = PostsModel.objects.filter(sender=one_user)[::-1]

    if request.method == "POST":
        follow = request.POST.get("follow")
        unfollow = request.POST.get("unfollow")
        send_message = request.POST.get("send_message")
        user = User.objects.get(id=request.user.id)
        edit_profile = request.POST.get("edit_profile")

        if follow:
            one_user.subscribers_set.add(request.user)
            user.subscription_set.add(one_user)
            one_user.exp += 10

            if (user in one_user.subscribers_set.all()) and (
                one_user in user.subscribers_set.all()
            ):
                user.friends_set.add(one_user)
                one_user.friends_set.add(user)

        elif unfollow:
            one_user.exp -= 10
            if (user in one_user.subscribers_set.all()) and (
                one_user in user.subscribers_set.all()
            ):
                user.friends_set.remove(one_user)
                one_user.friends_set.remove(user)

            one_user.subscribers_set.remove(request.user)
            user.subscription_set.remove(one_user)

        elif edit_profile:
            if one_user == request.user:
                return redirect(f"/settings")
        elif send_message:
            return redirect(f"/chat/{one_user.id}")
        else:
            reac(request)

        if one_user.exp >= 100:
            one_user.exp -= 100
            one_user.level += 1

        one_user.save()
        return redirect(f"/sc/user_profile/{id}")

    return render(
        request,
        "main/user_profile.html",
        context={
            "one_user": one_user,
            "next_level": next_level,
            "user_posts": user_posts,
            "total_unread_messages": unread_msg,
        }
    )




def ftf(request):
    return render(request, "main/404.html")



def get_unread_messages_count(request):
    user_chats = Chat.objects.filter(Q(member_1=request.user) | Q(member_2=request.user))
    
    total_unread_messages = 0
    for i in user_chats:
        i.unread_messages = i.messages.filter(viewed = False).exclude(sender = request.user).count()
        total_unread_messages += i.unread_messages
        i.save()
        
    return total_unread_messages
        
    

def download(request):
    if request.user.is_staff:
        temp_dir = tempfile.mkdtemp()
        temp_folder_path = os.path.join(temp_dir, "download")

        file_path = "db.sqlite3"
        media_folder_path = "media"

        os.makedirs(temp_folder_path)
        shutil.copy2(file_path, temp_folder_path)
        shutil.copytree(media_folder_path, os.path.join(temp_folder_path, "media"))

        zip_file_path = os.path.join(temp_dir, "download.zip")

        with zipfile.ZipFile(zip_file_path, "w") as zip_file:
            for root, dirs, files in os.walk(temp_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(
                        file_path, os.path.relpath(file_path, temp_folder_path)
                    )

        with open(zip_file_path, "rb") as f:
            zip_data = f.read()

        zip_buffer = BytesIO()
        zip_buffer.write(zip_data)
        zip_buffer.seek(0)

        response = FileResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="download.zip"'

        shutil.rmtree(temp_dir)

        return response
    else:
        return render(request, "ftf")


def upd_login(request):
    user_ = User.objects.get(id=request.user.id)
    user_.update_last_login(user_)
    user_.save()


def reac(request):
    """
    Likes / Dislikes / Comments

    """

    btn_l = request.POST.get("btn_l")
    btn_d = request.POST.get("btn_d")
    btn_f = request.POST.get("btn_f")

    user = User.objects.get(username=request.user.username)

    if btn_l:
        prod = PostsModel.objects.get(id=btn_l)
        post_sender = User.objects.get(id=prod.sender.id)

        if request.user in prod.likers.all():
            prod.likers.remove(request.user)
            if post_sender != user:
                post_sender.exp -= 1
                post_sender.points -= 1
                user.reactions -= 1

        else:
            prod.likers.add(request.user)
            if post_sender != user:
                post_sender.exp += 1
                post_sender.points += 1
                user.reactions += 1

            if request.user in prod.dislikers.all():
                prod.dislikers.remove(request.user)
                    
        post_sender.save()

    elif btn_d:
        prod = PostsModel.objects.get(id=btn_d)
        post_sender = User.objects.get(id=prod.sender.id)

        if request.user in prod.dislikers.all():
            prod.dislikers.remove(request.user)
            if post_sender != user:
                post_sender.points -= 1
                user.reactions -= 1

        else:
            prod.dislikers.add(request.user)
            if post_sender != user:
                post_sender.points += 1
                user.reactions += 1

            if request.user in prod.likers.all():
                prod.likers.remove(request.user)
        post_sender.save()

    elif btn_f:
        prod = PostsModel.objects.get(id=btn_f)

        if prod in user.favorites.all():
            user.favorites.remove(prod)

        else:
            user.favorites.add(prod)

        return redirect("posts")

    try:
        prod = PostsModel.objects.get(id=btn_l if btn_l else btn_d)
        post_sender = User.objects.get(id=prod.sender.id)

        if post_sender.exp >= 100:
            post_sender.exp -= 100
            post_sender.level += 1
        post_sender.save()
    except:
        pass

    try:
        prod.save()
        user.save()
    except:
        pass
