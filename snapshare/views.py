from django.shortcuts import redirect, render
from app.models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


@login_required
def home(request):
    current_user = request.user
    user_profile = Profile.objects.get(username = current_user)
    list = []

    # Following Users
    following_list = Follow.objects.filter(follower = user_profile)
    # for user in following_list:
    #     following_user = Profile.objects.get(username = user.following.username)
    #     list.append(following_user.username)
    # print(list)

    following_users = [follow.following.username for follow in following_list]
    # print(following_list)
    # print(following_users)

    # Posts of the following users
    feeds = Post.objects.filter(user__username__in=following_users)
    # post_id = [post.id for post in feeds]
    # print(post_id)

    # post_comments = Comment.objects.filter(post__in = post_id)
    # print(post_comments)

    # New users
    new_users = (
        Profile.objects.all()
        .exclude(username = current_user)
        .exclude(username__in = following_users)
        .order_by("-id")[0:5]
    )

    context = {
        "current_user": current_user,
        "feeds": feeds,
        "user_profile": user_profile,
        "suggested_users": new_users,
    }

    return render(request, "main/home.html", context)


@login_required
def profile(request, slug):
    user_profile = Profile.objects.get(slug=slug)
    user = user_profile.username
    account_type = user_profile.account_type
    # print(user_profile)

    # Count followers and following using annotations
    followers_list = Follow.objects.filter(following = user_profile)
    followers_count = followers_list.count()
    following_count = Follow.objects.filter(follower = user_profile).count()

    # Fetch user's posts
    posts = Post.objects.filter(user__username = user)
    post_count = posts.count()

    
    current_user = request.user
    # print(current_user)
    current_user_following = Follow.objects.filter(follower__username = current_user)
    current_user_following_user_list = [follow.following.username for follow in current_user_following]
    # print(current_user_following_user_list)

    user_profile_followers = [follow.follower.username for follow in followers_list]
    # print(user_profile_followers)

    followed_by = [name.username for name in current_user_following_user_list if name in user_profile_followers]
    # print(followed_by)

    sender = Profile.objects.get(username=current_user)
    follow_request = Notification.objects.filter(
            sender = sender, user = user_profile, notification_type = 3
        ).exists()
    follow_request_accepted = Notification.objects.filter(
            sender = sender, user = user_profile, notification_type = 3, is_seen = True
        ).exists()
    
    # if follow_notification:
    # try:
    #     follow_request = Notification.objects.get(sender = sender, user = user_profile, notification_type = 3)
    # except ObjectDoesNotExist:
    #     follow_request = "False"

    context = {
        "user_profile": user_profile,
        "slug_user": user,
        "current_user": current_user,
        "followers_count": followers_count,
        "following_count": following_count,
        "post_count": post_count,
        "current_user_following_user_list": current_user_following_user_list,
        'followed_by': followed_by,
        'account_type': account_type,
        "posts": posts,
        'follow_request':follow_request,
        'follow_request_accepted': follow_request_accepted,
    }

    return render(request, "main/profile.html", context)

@login_required
def single_post(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post = post)
    context = {
        "post": post,
        "comments": comments,
    }
    return render(request, "main/post.html", context)

def ShowNotification(request):
    current_user = request.user
    user = Profile.objects.get(username = current_user)
    notifications = Notification.objects.filter(user=user).order_by('-date')
    print(notifications)

    context = {
        'notifications': notifications,
    }
    return render(request, 'main/notification.html', context)

def DeleteNotification(request, notify_id):
    current_user = request.user
    user = Profile.objects.get(username = current_user)
    Notification.objects.filter(id=notify_id, user=user).delete()
    return redirect('show_notifications')
