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
    path('create_channel/<str:pk>', views_reg.create_channel, name='create_channel'),
    path('edit_channel/<str:pk>', views_reg.edit_channel, name='edit_channel'),
    
    path('video/<str:pk>', views_tube.watch_video),
    path('channel/<str:pk>', views_tube.channnel_view),
    path('playlist/<str:pk>', views_tube.playlist),
    path('watchlater/<str:pk>', views_tube.watchlater),
    
    path('subscribe', views_tube.subscribe, name='subscribe'), 
    path('unsubscribe', views_tube.unsubscribe, name='unsubscribe'), 
    path('like', views_tube.like, name='like'), 
    path('dislike', views_tube.dislike, name='dislike'), 
    path('unlike', views_tube.unlike, name='unlike'), 
    path('undislike', views_tube.undislike, name='undislike'), 
    
    path('viewers',views_tube.all_viewers),
    path('get_viewers',views_tube.get_viewers, name='get_viewers'),
    path('get_subs/<str:pk>',views_tube.get_subs, name='get_subs'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Admin Panel | K TUBE"
admin.site.site_title = "Admin | K TUBE"
admin.site.index_title = "Adminstration | K TUBE"
