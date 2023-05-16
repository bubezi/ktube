from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from tube import views as views_tube
from register import views as views_reg

urlpatterns = [
    path('', views_tube.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('bye', views_reg.bye_page, name="bye"),
    path('register', views_reg.register, name="register"),
    path('profile', views_reg.profile_page, name='profile'),
    
    path('library', views_tube.library, name="library"),
    path('watchlater', views_tube.watchlater, name="watchlater"),
    path('liked_videos', views_tube.liked_videos, name="liked_videos"),
    path('history', views_tube.history, name="history"),
    path('saved_playlists', views_tube.saved_playlists, name="saved_playlists"),
    
    path('subscriptions', views_tube.subscriptions, name="subscriptions"),
    path('create_channel', views_reg.create_channel, name="create_channel"),
    path('subscribe', views_tube.subscribe, name='subscribe'), 
    path('unsubscribe', views_tube.unsubscribe, name='unsubscribe'), 
    path('like', views_tube.like, name='like'), 
    path('dislike', views_tube.dislike, name='dislike'), 
    path('unlike', views_tube.unlike, name='unlike'), 
    path('undislike', views_tube.undislike, name='undislike'), 
    path('add_view', views_tube.add_view, name='add_view'), 
    
    path('viewers',views_tube.all_viewers, name='viewers'),
    path('get_viewers',views_tube.get_viewers, name='get_viewers'),
    
    path('add_video_to_playlist',views_tube.add_video_to_playlist, name='add_video_to_playlist'),
    
    ## The following are associated with a specific channel
    path('edit_channel/<str:pk>', views_reg.edit_channel),
    path('video/<str:pk>', views_tube.watch_video),
    path('channel/<str:pk>', views_tube.channnel_view),
    path('playlist/<str:pk>', views_tube.playlist),
    path('upload/<str:pk>', views_tube.upload_video),
    path('create_playlist/<str:pk>', views_tube.create_playlist),
    
    path('get_subs/<str:pk>',views_tube.get_subs),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Admin Panel | K TUBE"
admin.site.site_title = "Admin | K TUBE"
admin.site.index_title = "Adminstration | K TUBE"
