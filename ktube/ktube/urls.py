from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from tube import views as views_tube
from register import views as views_reg

from django.views.generic import TemplateView

urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
    path('', views_tube.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),


    
    path('bye', views_reg.bye_page, name="bye"),
    path('register', views_reg.register, name="register"),
    path('profile', views_reg.profile_page, name='profile'),
    path('create_channel', views_reg.create_channel, name="create_channel"),
    path('edit_channel/<str:pk>', views_reg.edit_channel, name="edit_channel"),    
    
    path('deposit', views_tube.deposit_view, name="deposit"),
    path('deposit_funds', views_tube.deposit_funds, name="deposit_funds"),
    
    
    path('library', views_tube.library, name="library"),
    path('watchlater', views_tube.watchlater, name="watchlater"),
    path('liked_videos', views_tube.liked_videos, name="liked_videos"),
    path('history', views_tube.history, name="history"),
    path('saved_playlists', views_tube.saved_playlists, name="saved_playlists"),
    path('save_playlist', views_tube.save_playlist, name="save_playlist"),
    path('unsave_playlist', views_tube.unsave_playlist, name="unsave_playlist"),
    
    path('delete_playlist', views_tube.delete_playlist, name="delete_playlist"),
    path('delete_video', views_tube.delete_video, name="delete_video"),
    path('delete_channel', views_tube.delete_channel, name="delete_channel"),
    path('delete_comment', views_tube.delete_comment, name="delete_comment"),
    path('delete_comment_reply', views_tube.delete_comment_reply, name="delete_comment_reply"),
    
    path('edit_playlist_v/<str:pk>', views_tube.edit_playlist_view, name="edit_playlist_view"),
    path('edit_playlist', views_tube.edit_playlist, name="edit_playlist"),
    
    path('edit_video_v/<str:pk>', views_tube.edit_video_view, name="edit_video_view"),
    path('edit_video', views_tube.edit_video, name="edit_video"),
    
    path('authenticate_action', views_tube.authenticate_action, name="authenticate_action"),
    
    
    path('delete_account', views_tube.delete_account, name="delete_account"),
    
    
    path('subscriptions', views_tube.subscriptions, name="subscriptions"),
    path('subscribe', views_tube.subscribe, name='subscribe'), 
    path('unsubscribe', views_tube.unsubscribe, name='unsubscribe'), 
    path('like', views_tube.like, name='like'), 
    path('dislike', views_tube.dislike, name='dislike'), 
    path('unlike', views_tube.unlike, name='unlike'), 
    path('undislike', views_tube.undislike, name='undislike'), 
    path('add_view', views_tube.add_view, name='add_view'), 
    path('comment', views_tube.comment, name='comment'), 
    path('reply_comment', views_tube.reply_comment, name='reply_comment'), 
    path('comment_many_channels', views_tube.comment_many_channels, name='comment_many_channels'), 
    path('reply_comment_many_channels', views_tube.reply_comment_many_channels, name='reply_comment_many_channels'), 
    
    path('like_comment', views_tube.like_comment, name='like_comment'), 
    path('dislike_comment', views_tube.dislike_comment, name='dislike_comment'), 
    
    path('viewers',views_tube.all_viewers, name='viewers'),
    path('get_viewers',views_tube.get_viewers, name='get_viewers'),
    
    path('add_video_to_playlist',views_tube.add_video_to_playlist, name='add_video_to_playlist'),
    path('remove_video_from_playlist',views_tube.remove_video_from_playlist, name='remove_video_from_playlist'),
    
    path('add_video_to_watchlater',views_tube.add_video_to_watchlater, name='add_video_to_watchlater'),
    path('remove_video_from_watchlater',views_tube.remove_video_from_watchlater, name='remove_video_from_watchlater'),
    
    path('search',views_tube.search_results_view, name='search'),
    path('my_channels',views_tube.my_channels_page, name='my_channels'),

    path('video/<str:pk>', views_tube.watch_video, name="video"),
    path('create_playlist/<str:pk>', views_tube.create_playlist, name="create_playlist"),
    path('channel/<str:pk>', views_tube.channnel_view, name="channel"),
    path('upload/<str:pk>', views_tube.upload_video, name="upload"),
    
    path('get_subs/<str:pk>',views_tube.get_subs, name="get_subs"),
    
    path('playlist/<str:pk>', views_tube.playlist, name="playlist"),
    path('watch_playlist/<str:pk>/<str:number>', views_tube.watch_playlist, name="watch_playlist"),
    
    path('get_views/<str:pk>',views_tube.get_views, name="get_views"),

    path('go_live', views_tube.go_live, name="go_live"),
    path('start_stream', views_tube.start_stream, name="start_stream"),
    path('stop_stream', views_tube.stop_stream, name="stop_stream"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Admin Panel | K TUBE"
admin.site.site_title = "Admin | K TUBE"
admin.site.index_title = "Adminstration | K TUBE"
