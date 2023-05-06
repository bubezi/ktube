"""
URL configuration for ktube project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from tube import views
from register import views as views_reg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    
    
    path('bye', views_reg.bye_page, name="bye"),
    path('register', views_reg.register, name="register"),
    path('profile', views_reg.profile_page, name='profile'),
    path('create_channel/<str:pk>', views_reg.create_channel, name='create_channel'),
    path('change_channel_details/<str:pk>', views_reg.change_channel_details, name='change_channel_details'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('video/<str:pk>', views.watch_video),
    path('channel/<str:pk>', views.channnel_view),
    path('playlist/<str:pk>', views.playlist),
    path('watchlater/<str:pk>', views.watchlater),
    path('subscribec/<str:pk>', views.subsribe_from_channel),
    path('subscribev/<str:video>/<str:pk>', views.subsribe_from_video),
    path('unsubscribec/<str:pk>', views.unsubsribe_from_channel),
    path('unsubscribev/<str:video>/<str:pk>', views.unsubsribe_from_video),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Admin Panel | K TUBE"
admin.site.site_title = "Admin | K TUBE"
admin.site.index_title = "Adminstration | K TUBE"
