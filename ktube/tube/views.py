from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .filters import VideoFilter
from .models import *


# Create your views here.
def home_view(request):
    videos = Video.objects.filter(private=False, unlisted=False)
    myFilter = VideoFilter(request.GET, queryset=videos)
    context = {'videos': videos, 'myFilter': myFilter, }
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = False
        except:
            context['no_channel'] = True       
    return render(request, 'tube/home.html', context)


def watch_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
    except Video.DoesNotExist:
        return HttpResponseBadRequest('<h1>404 Not Found</h1><h3>Video Does Not Exist! SORRYYY</h3>')  
    
    if video.private:
        if request.user.is_authenticated:
            try:
                viewer = request.user.viewer
                if not video.channel.user == viewer: # type: ignore
                    return HttpResponseForbidden('<h1>Forbidden</h1><h4>Video is private</h4>')
            except:
                return HttpResponseForbidden('<h1>Forbidden</h1><h4>Video is private</h4>')
        else:
            return HttpResponseForbidden('<h1>Forbidden</h1><h4>Video is private</h4>')  

    subscriber_count = video.channel.subscribers.count() # type: ignore
    comments = Comment.objects.filter(video=video)
    comment_replies = CommentReply.objects.all()
    
    paginator = Paginator(comments, 10) # 10 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # replies_dict = comment_replies.in_bulk()
    # replies_list = []
    # for key in range(len(replies_dict)):
    #     replies_list.append(replies_dict[key+1].reply) # replies here are strings
    context = {"video": video, "comments": page_obj, "comment_replies": comment_replies,
               "subscriber_count": subscriber_count}
    
                
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            if video.channel.subscribers.contains(viewer): # type: ignore
                context['subscribed']=True
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['no_channel'] = True
                context['many_channels'] = False
            except:
                context['many_channels'] = True
                context['no_channel'] = False
        except:
            context['many_channels'] = False
            context['no_channel'] = True
    
    return render(request, 'tube/watch.html', context)


def channnel_view(request, pk):
    try:    
        channel = Channel.objects.get(id=pk)
    except Channel.DoesNotExist:
        return HttpResponse('<h1>404 Not Found</h1><h4>Channel Does Not Exist! SORRYYY</h4>')  
    videos = Video.objects.filter(channel=channel, unlisted=False, private=False)
    subscriber_count = channel.subscribers.count()
    playlists = Playlist.objects.filter(channel=channel, public=True) 
    context = {'channel': channel, "videos": videos, "subscriber_count": subscriber_count,
               'playlists': playlists} 
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            if channel.subscribers.contains(viewer):
                context['subscribed']=True
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                unlisted_videos = Video.objects.filter(channel=channel, unlisted=True)
                private_videos = Video.objects.filter(channel=channel, private=True)
                private_playlists = Playlist.objects.filter(channel=channel, public=False)
                context['unlisted_videos'] = unlisted_videos
                context['private_videos'] = private_videos
                context['private_playlists'] = private_playlists
                context['many_channels'] = False
            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = False
        except:
            context['no_channel'] = True
    return render(request, 'tube/channel.html', context)


def playlist(request, pk):
    context = {}
    if request.user.is_authenticated:
        try:
            playlist = Playlist.objects.get(id=pk)
        except Playlist.DoesNotExist:
            return HttpResponse('<h1>404 Not Found</h1><h4>Playlist Does Not Exist! SORRYYY</h4>')
        videos=playlist.videos.filter(private=False)
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            if not playlist.public:
                if not playlist.channel.user == viewer: # type: ignore 
                    return HttpResponseForbidden("<h1>Forbidden</h1><h4>Playlist is private</h4>")
                
            if playlist.channel.user == viewer: # type: ignore 
                videos=playlist.videos.all()
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = False
        except:
            context['no_channel'] = True 
        

        context['playlist']=playlist 
        context["videos"]  =videos
    else:
        try:
            playlist = Playlist.objects.get(id=pk)
        except Playlist.DoesNotExist:
            return HttpResponse('<h1>404 Not Found</h1><h4>Playlist Does Not Exist! SORRYYY</h4>')
        if not playlist.public:
            return HttpResponseForbidden("<h1>Forbidden</h1><h4>Playlist is private</h4>")

        videos=playlist.videos.filter(private=False)
        context['playlist']=playlist 
        context["videos"]  =videos
        context['many_channels'] = False
        context['no_channel'] = True
    return render(request, 'tube/playlist.html', context)


def watchlater(request, pk):
    if request.user.is_authenticated:
        context = {}
        try:
            watchlater = Watchlater.objects.get(id=pk)
        except Watchlater.DoesNotExist as e:
            return HttpResponseBadRequest(e)
        videos = watchlater.videos.all()
        context['videos']=videos
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            if not viewer == watchlater.viewer:
                return HttpResponseForbidden('<h1>Forbidden</h1><h4>You have no access to This Watch later playlist</h4>')        
            try:
                nav_channel = Channel.objects.get(user=viewer)
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False
            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True
            except:
                context['many_channels'] = True
                context['no_channel'] = False
        except:
            context['no_channel'] = True      
        context['watchlater'] = watchlater
        return render(request, 'tube/watchlater.html', context)
    else:
        return redirect('login')
    
    
def subsribe_from_channel(request, pk):
    if request.user.is_authenticated:
        try:
            channel = Channel.objects.get(id=pk)
            try:
                viewer = request.user.viewer
                if channel.user == viewer: # type: ignore
                    return HttpResponseForbidden('<h1>Forbidden</h1><h4>You cannot subscribe to your own channel</h4>')
                else:
                    channel.subscribers.add(viewer)
                    return redirect(f'/channel/{pk}')
            except:
                return redirect('login')
        except Channel.DoesNotExist:
            return HttpResponseBadRequest('<h1>404 Not Found</h1><h4>Channel Does Not Exist</h4>')
    else:
        return redirect('login')
 
    
def subsribe_from_video(request, video, pk):
    if request.user.is_authenticated:
        try:
            channel = Channel.objects.get(id=pk)
            try:
                viewer = request.user.viewer
                if channel.user == viewer: # type: ignore
                    return HttpResponseForbidden('<h1>Forbidden</h1><h4>You cannot subscribe to your own channel</h4>')
                else:
                    channel.subscribers.add(viewer)
                    return redirect(f'/video/{video}')
            except:
                return redirect('login')
        except Channel.DoesNotExist:
            return HttpResponseBadRequest('<h1>Forbidden</h1><h4>Channel Does Not Exist</h4>')
    else:
        return redirect('login')
    

def unsubsribe_from_channel(request, pk):
    if request.user.is_authenticated:
        try:
            channel = Channel.objects.get(id=pk)
            try:
                viewer = request.user.viewer
                if channel.user == viewer: # type: ignore
                    return HttpResponseForbidden('<h1>Forbidden</h1><h4>You cannot subscribe to your own channel</h4>')
                else:
                    channel.subscribers.remove(viewer)
                    return redirect(f'/channel/{pk}')
            except:
                return redirect('login')
        except Channel.DoesNotExist:
            return HttpResponseBadRequest('<h1>Forbidden</h1><h4>Channel Does Not Exist</h4>')
    else:
        return redirect('login')
 
    
def unsubsribe_from_video(request, video, pk):
    if request.user.is_authenticated:
        try:
            channel = Channel.objects.get(id=pk)
            try:
                viewer = request.user.viewer
                if channel.user == viewer: # type: ignore
                    return HttpResponseForbidden('<h1>Forbidden</h1><h4>You cannot subscribe to your own channel</h4>')
                else:
                    channel.subscribers.remove(viewer)
                    return redirect(f'/video/{video}')
            except:
                return redirect('login')
        except Channel.DoesNotExist:
            return HttpResponseBadRequest('<h1>404 Not Found</h1><h4>Channel Does Not Exist</h4>')
    else:
        return redirect('login')
