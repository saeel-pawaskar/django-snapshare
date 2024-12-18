from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            User.objects.filter(username=username).exists()
            return redirect("register")

        else:
            user = User.objects.create_user(
                email=email, username=username, password=password
            )
            user.save()

            new_user = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                username = new_user,
                fullname = fullname,
            )
            new_profile.save()

            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        return render(request, "registration/register.html")


def login_auth(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password is incorrect.")
            return redirect("login_auth")
    else:
        return render(request, "registration/login.html")


@login_required
def update_profile(request):
    current_user = request.user
    user = User.objects.get(username = current_user)
    user_profile = Profile.objects.get(username = current_user)

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_fullname = request.POST.get("fullname")
        new_profile_picture = request.FILES.get("profile_picture")
        new_bio = request.POST.get("bio") 

        # Update user profile
        if user_profile:
            user_profile.fullname = new_fullname
            user_profile.bio = new_bio

            if new_profile_picture:
                user_profile.profile_picture = new_profile_picture

            user_profile.save()

        # Update username if changed
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile", slug=user_profile.slug)
    
    else:
        return render(
            request, "postdata/update_profile.html", {"user_profile": user_profile}
        )


@login_required
def create_post(request):
    if request.method == "POST":
        current_user = request.user

        user = Profile.objects.get(username = current_user)
        image = request.FILES.get("image")
        caption = request.POST.get("caption")

        post = Post.objects.create(
            user = user,
            image = image,
            caption = caption,
        )
        post.save()

        messages.success(request, "Post created successfully.")
        return redirect("profile", slug=user.slug)
    else:
        return render(request, "postdata/create_post.html")
    
@login_required
def follow_request(request):
    if request.method == 'POST':
        current_user = request.user
        target_user = request.POST.get("username")
        source_page = request.POST.get("source_page")

        sender = Profile.objects.get(username=current_user)
        user = Profile.objects.get(username__username=target_user)

        notification = Notification.objects.filter(
            sender = sender, user = user, notification_type = 3
        ).exists()

        if not notification:
            notification = Notification.objects.create(
                sender = sender,
                user = user,
                notification_type = 3,
                text_preview = f"{sender.username.username} requested to follow you."
            )
            notification.save()

        else:
            notification = Notification.objects.get(
                sender = sender,
                user = user,
                notification_type = 3,
            )
            notification.delete()
            
            Follow.objects.filter(follower = sender, following = user).delete()


        if source_page == "home":
            return redirect('home')
        elif source_page == "profile":
            return redirect("profile", slug=user.slug)
        
def accept_request(request):
    if request.method == 'POST':
        current_user = request.user
        username = request.POST.get("username")

        following_user = Profile.objects.get(username = current_user)
        follower = Profile.objects.get(username__username = username)

        Follow.objects.create(follower = follower, following = following_user).save()

        follow_request = Notification.objects.filter(sender = follower, user = following_user, notification_type = 3).exists()

        if follow_request:
            follow_request = Notification.objects.get(sender = follower, user = following_user, notification_type = 3)
            follow_request.is_seen = True
            follow_request.save()

        return redirect("show_notifications")
        

@login_required
def following(request):
    if request.method == "POST":
        current_user = request.user
        username = request.POST.get("username")
        source_page = request.POST.get("source_page")

        follower = Profile.objects.get(username = current_user)
        following_user = Profile.objects.get(username__username = username)

        # Check if the follow relationship already exists
        follow = Follow.objects.filter(follower = follower, following = following_user).exists()

        if not follow:
            Follow.objects.create(follower = follower, following = following_user)
            Notification.objects.create(
                sender=follower, user=following_user, notification_type = 4,
                text_preview = f"{follower.username} started following you."
                ).save()
        else:
            Follow.objects.filter(follower = follower, following = following_user).delete()
            Notification.objects.get(
                sender=follower, user=following_user, notification_type = 4,
                ).delete()

        if source_page == "home":
            return redirect('home')
        elif source_page == "profile":
            return redirect("profile", slug=following_user.slug)

@login_required
def like(request, post_id):
    current_user = request.user
    sender = Profile.objects.get(username=current_user)
    post = Post.objects.get(id=post_id)
    user = Profile.objects.get(username=post.user.username)

    current_likes = post.likes
    liked = Like.objects.filter(user=sender, post=post).exists()

    if not liked:
        Like.objects.create(user=sender, post=post)
        current_likes += 1

        # Create notification
        Notification.objects.create(
            post=post, sender=sender, user=user, notification_type=1,
            text_preview=f"{sender.username} liked your post."
        )
    else:
        Like.objects.filter(user=sender, post=post).delete()
        current_likes -= 1

        # Delete notification
        Notification.objects.filter(
            post=post, sender=sender, user=user, notification_type=1
        ).delete()

    post.likes = current_likes
    post.save()

    return redirect('home')



@login_required
def comments(request, id):
    if request.method == "POST":
        current_user = request.user

        user = Profile.objects.get(username = current_user)
        post = Post.objects.get(id = id)
        post_user = Profile.objects.get(username = post.user.username)
        comment = request.POST.get("comment")
        source_page = request.POST.get("source_page")

        comment = Comment.objects.create(
            user=user,
            post=post,
            comment=comment,
        )
        comment.save()

        notification = Notification.objects.create(
            post=post, sender=user, user=post_user, notification_type = 2,
            text_preview = f"{user.username} commented: {comment.comment}."
        )
        notification.save()

        if source_page == "home":
            return redirect("home")
        elif source_page == "profile":
            return redirect("post", slug=post.slug)


@login_required
def search(request):
    if request.method == "POST":
        search_user = request.POST.get("search")
        user_profile = Profile.objects.filter(
            Q(username__username__icontains = search_user) | Q(fullname__icontains = search_user)
        ).exclude(username = request.user)
        context = {
            "user_profile": user_profile,
        }
        return render(request, "main/search.html", context)
    else:
        return render(request, "main/search.html")

@login_required   
def settings(request):
    current_user = request.user
    profile = Profile.objects.get(username = current_user)
    account = profile.account_type
    
    if request.method == 'POST':
        account_type = request.POST.get('account_type')

        profile.account_type = account_type
        profile.save()

        return redirect('settings')
    else:
        return render(request, 'postdata/settings.html', {'account': account})