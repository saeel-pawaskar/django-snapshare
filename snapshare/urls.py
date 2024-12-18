from django.contrib import admin
from django.urls import path,include
from .import views,user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_auth/', user_views.login_auth, name='login_auth'),

    path('', views.home, name='home'),

    path('<slug:slug>/', views.profile, name='profile'),
    path('accounts/edit/', user_views.update_profile, name='update_profile'),

    path('accounts/create/', user_views.create_post, name='create_post'),
    path('p/<slug:slug>', views.single_post, name='post'),


    path('accounts/follow_request/', user_views.follow_request, name='follow_request'),
    path('accounts/accept_request/', user_views.accept_request, name='accept_request'),
    path('accounts/follow/', user_views.following, name='follow'),
    path('p/like/<int:post_id>', user_views.like, name='like'),
    path('accounts/comment/<int:id>/', user_views.comments, name='comment'),

    path('accounts/search/', user_views.search, name='search'),

    path('accounts/privacy_settings/', user_views.settings, name='settings'),

    path('accounts/notifications/', views.ShowNotification, name='show_notifications'),
    path('accounts/delete_notification/<int:notify_id>', views.DeleteNotification, name='delete_notification'),

        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
