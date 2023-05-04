from django.shortcuts import render
from .models import *
from .filters import VideoFilter
from django.http import HttpResponse


# Create your views here.
def home_view(request):
    videos = Video.objects.all()
    
    myFilter = VideoFilter(request.GET, queryset=videos)
        
    context = {'videos': videos, 'myFilter': myFilter, }
        
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = True
        except:
            context['no_channel'] = True
                
    return render(request, 'tube/home.html', context)


def watch_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
    except Video.DoesNotExist:
        return HttpResponse('Video Does Not Exist! SORRYYY')
    
    subscriber_count = video.channel.subscribers.count() # ignore pylance 
    comments = Comment.objects.filter(video=video)
    comment_replies = CommentReply.objects.all()
    replies_dict = comment_replies.in_bulk()
    replies_list = []
    for key in range(len(replies_dict)):
        replies_list.append(replies_dict[key+1].reply) # replies here are strings
    
    context = {"video": video, "comments": comments, "comment_replies": comment_replies,
               "subscriber_count": subscriber_count}

    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = True
        except:
            context['no_channel'] = True
    
    return render(request, 'tube/watch.html', context)


def channnel_view(request, pk):
    try:    
        channel = Channel.objects.get(id=pk)
    except Channel.DoesNotExist:
        return HttpResponse('Channel Does Not Exist! SORRYYY')
    
    videos = Video.objects.filter(channel=channel)
    subscriber_count = channel.subscribers.count()
    playlists = Playlist.objects.filter(channel=channel)
        
    context = {'channel': channel, "videos": videos, "subscriber_count": subscriber_count,
               'playlists': playlists} 
    
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = True
        except:
            context['no_channel'] = True
        
    return render(request, 'tube/channel.html', context)

def playlist(request, pk):
    try:
        playlist = Playlist.objects.get(id=pk)
    except Playlist.DoesNotExist:
        return HttpResponse('Playlist Does Not Exist! SORRYYY')
    
    videos=playlist.videos.all()
    context = {'playlist':playlist, "videos":videos}
    
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = True
        except:
            context['no_channel'] = True
        
    return render(request, 'tube/playlist.html', context)
