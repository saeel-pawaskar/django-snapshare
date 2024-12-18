# Generated by Django 4.2.5 on 2024-10-16 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=50, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='profile_picture/default.png', null=True, upload_to='profile_picture/')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('account_type', models.CharField(blank=True, choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=7, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_image/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField(blank=True, choices=[(1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Following')], null=True)),
                ('text_preview', models.CharField(blank=True, max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_post', to='app.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_from_user', to='app.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_to_user', to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='app.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='app.profile')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='app.profile')),
            ],
            options={
                'verbose_name': 'Follow',
                'verbose_name_plural': 'Follows',
                'unique_together': {('follower', 'following')},
            },
        ),
    ]