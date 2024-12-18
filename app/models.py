from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True, default='profile_picture/default.png')
    bio = models.TextField(max_length=500, blank=True)
    account_type = models.CharField(max_length=7, choices=ACCOUNT_TYPE_CHOICES, default='public', null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.username.username)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.fullname:
            return f"{self.fullname}"
        else:
            return f"{self.username.username}"
    
class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='post_image/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%B %d')}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_slug()
        super().save(*args, **kwargs)

    def create_slug(self, new_slug= None):
        if self.image:
            slug = slugify(self.image.name)
        if new_slug is not None:
            slug = new_slug
        slug_exists = Post.objects.filter(slug=slug).exists()
        if slug_exists:
            post = Post.objects.filter(slug=slug).order_by('-id').first()
            new_slug = f"{slug}-{post.id + 1}"
            return self.create_slug(new_slug=new_slug)
        return slug

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        unique_together = ('follower', 'following')

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return f"{self.user.username} liked {self.post.user.username} post."

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented '{self.comment[:20]}' on {self.post.user.username}'s post"
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Like'), 
        (2, 'Comment'), 
        (3, 'Follow'),
        (4, 'Following'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE,  null=True, blank=True, related_name="notification_post")
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="notification_from_user")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="notification_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES, null=True, blank=True)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification from {self.sender} to {self.user} - {self.get_notification_type_display()}'