from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import VideoForm, PlaylistForm
from register.utils import check_errors
from .filters import VideoFilter
from .models import *


##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################           VIEWS FUNCTIONS         ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


def home_view(request):
    videos = Video.objects.filter(private=False, unlisted=False) # type: ignore
    myFilter = VideoFilter(request.GET, queryset=videos)
    context = {'videos': videos, 'myFilter': myFilter, }

    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater

            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel)  # type: ignore
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['no_channel'] = True
                context['many_channels'] = False

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
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
    
    more_videos = Video.objects.all()
    context['more_videos'] = more_videos
    
                
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater
            
            if video.channel.subscribers.contains(viewer): # type: ignore
                context['subscribed']=True
                
            try:
                likes = LikedVideos.objects.get(viewer=viewer)
                dislikes = DisLikedVideos.objects.get(viewer=viewer)
  
            except:
                likes = LikedVideos(viewer=viewer)
                dislikes = DisLikedVideos(viewer=viewer)
                likes.save()
                dislikes.save()
                
            if likes.videos.contains(video):
                context['liked'] = True

            if dislikes.videos.contains(video):
                context['disliked'] = True
                
            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['no_channel'] = True
                context['many_channels'] = False

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['many_channels'] = False
            context['no_channel'] = True
    
    return render(request, 'tube/watch.html', context)



def watch_playlist(request, pk, number):
    try:
        playlist = Playlist.objects.get(id=pk)

    except Playlist.DoesNotExist:
        return HttpResponseBadRequest('<h1>404 Not Found</h1><h3>Playlist Does Not Exist! SORRYYY</h3>')  
    
    if not playlist.public:
        if request.user.is_authenticated:
            try:
                viewer = request.user.viewer
                if not playlist.channel.user == viewer: # type: ignore
                    return HttpResponseForbidden('<h1>Forbidden</h1><h4>Playlist is private</h4>')

            except:
                return HttpResponseForbidden('<h1>Forbidden</h1><h4>Playlist is private</h4>')

        else:
            return HttpResponseForbidden('<h1>Forbidden</h1><h4>Playlist is private</h4>') 
        
        
        
        #### The Patient Predator
    try:
        videos = []
        videos_dict = playlist.videos.all()
        
        for video in videos_dict:
            videos.append(video)
        number = int(number)
        video = videos[number]

    except:
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

    context = {"video": video, "comments": page_obj, "comment_replies": comment_replies,
               "subscriber_count": subscriber_count}
    
    
    
    more_videos = Video.objects.all()
    context['more_videos'] = more_videos
    
    
    context['playlist_videos'] = videos
    
    
    
    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater
            
            if video.channel.subscribers.contains(viewer): # type: ignore
                context['subscribed']=True
                
            try:
                likes = LikedVideos.objects.get(viewer=viewer)
                dislikes = DisLikedVideos.objects.get(viewer=viewer)
  
            except:
                likes = LikedVideos(viewer=viewer)
                dislikes = DisLikedVideos(viewer=viewer)
                likes.save()
                dislikes.save()
                
            if likes.videos.contains(video):
                context['liked'] = True

            if dislikes.videos.contains(video):
                context['disliked'] = True
                
            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['no_channel'] = True
                context['many_channels'] = False

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
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
    context['playlist_owner']=False

    if request.user.is_authenticated:
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer

            if channel.user == viewer:
                context['playlist_owner']= True
                
            if channel.subscribers.contains(viewer):
                context['subscribed']=True
                
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                
            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
            context['watchlater'] = watchlater
                
            try:
                saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
            except SavedPlaylists.DoesNotExist:
                saved_playlists = SavedPlaylists(viewer=viewer)
                saved_playlists.save()
            context['saved_playlists'] = saved_playlists.playlists.all()


            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
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
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True
    return render(request, 'tube/channel.html', context)


def playlist(request, pk):
    context = {}
    context['playlist_owner'] = False
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
                context['playlist_owner'] = True
                
            
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                
            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
            context['watchlater'] = watchlater
                
            try:
                saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
            except SavedPlaylists.DoesNotExist:
                saved_playlists = SavedPlaylists(viewer=viewer)
                saved_playlists.save()
            context['saved_playlists'] = saved_playlists.playlists.all()

            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['many_channels'] = False
            context['no_channel'] = True 
        

        context['playlist']=playlist 
        context["videos"]  =videos

    else:
        try:
            playlist = Playlist.objects.get(id=pk)

        except Playlist.DoesNotExist:
            return HttpResponse('<h1>404 Not Found</h1><h4>Playlist Does Not Exist! SORRYYY</h4>')

        if not playlist.public:
            return redirect('login')

        videos=playlist.videos.filter(private=False)
        context['playlist']=playlist 
        context["videos"]  =videos
        context['many_channels'] = False
        context['no_channel'] = True
    return render(request, 'tube/playlist.html', context)


def watchlater(request):
    if request.user.is_authenticated:
        context = {}

        try:
            viewer = request.user.viewer
            context['viewer'] = viewer

            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater
            context['videos']=watchlater.videos.all()  
            
            

            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False  

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True      
        
        return render(request, 'tube/watchlater.html', context)

    else:
        return redirect('login')


def liked_videos(request):
    if request.user.is_authenticated:
        context = {}

        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater

            try:
                liked_videos = LikedVideos.objects.get(viewer=viewer)
                context['liked_videos'] = liked_videos

            except LikedVideos.DoesNotExist:
                liked_videos = LikedVideos(viewer=viewer)
                liked_videos.save()
                context['liked_videos'] = liked_videos
            context['videos']=liked_videos.videos.all()

            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True        
        return render(request, 'tube/liked_videos.html', context)

    else:
        return redirect('login')


def history(request):
    if request.user.is_authenticated:
        context = {}

        try:
            viewer = request.user.viewer
            context['viewer'] = viewer

            try:
                history = History.objects.get(viewer=viewer)
                context['history'] = history

            except History.DoesNotExist:
                history = History(viewer=viewer)
                history.save()
                context['history'] = history
            views = history.views.order_by('viewed_on')
            views = views.reverse()
            context['views']=views

            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater
            context['videos']=watchlater.videos.all()  
            

            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True        
        return render(request, 'tube/history.html', context)

    else:
        return redirect('login')


def saved_playlists(request):
    if request.user.is_authenticated:
        context = {}

        try:
            viewer = request.user.viewer
            context['viewer'] = viewer

            try:
                saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
                context['saved_playlists'] = saved_playlists

            except SavedPlaylists.DoesNotExist:
                saved_playlists = SavedPlaylists(viewer=viewer)
                saved_playlists.save()
                context['saved_playlists'] = saved_playlists

            context['playlists']=saved_playlists.playlists.all()

            try:
                nav_channel = Channel.objects.get(user=viewer)
                my_playlists = Playlist.objects.filter(channel=nav_channel)
                context['my_playlists'] = my_playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)

                context['my_playlists'] =  my_playlists
                context['my_channels'] =  my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True        

        context['playlist_owner'] = True

        return render(request, 'tube/saved_playlists.html', context)

    else:
        return redirect('login')
 
 
def library(request):
    if request.user.is_authenticated:
        context = {}

        try:
            viewer = request.user.viewer
            context['viewer'] = viewer

            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater

            try:
                liked_videos = LikedVideos.objects.get(viewer=viewer)
                context['liked_videos'] = liked_videos

            except LikedVideos.DoesNotExist:
                liked_videos = LikedVideos(viewer=viewer)
                liked_videos.save()
                context['liked_videos'] = liked_videos

            try:
                history = History.objects.get(viewer=viewer)
                context['history'] = history
                history_views = history.views.order_by('viewed_on')
                history_views = history_views.reverse()

            except History.DoesNotExist:
                history = History(viewer=viewer)
                history.save()
                history_views = history.views.order_by('viewed_on')
                history_views = history_views.reverse()
                context['history'] = history

            try:
                saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
                context['saved_playlists'] = saved_playlists

            except SavedPlaylists.DoesNotExist:
                saved_playlists = SavedPlaylists(viewer=viewer)
                saved_playlists.save()
                context['saved_playlists'] = saved_playlists

            context['history_views']=history_views
            context['playlists']=saved_playlists.playlists.all()
            context['liked_videos_videos']=liked_videos.videos.all()
            context['watchlater_videos']=watchlater.videos.all()     

            try:
                nav_channel = Channel.objects.get(user=viewer)
                my_playlists = Playlist.objects.filter(channel=nav_channel)
                context['my_playlists'] = my_playlists
                context['nav_channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)

                context['my_playlists'] =  my_playlists
                context['my_channels'] =  my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = False
            context['no_channel'] = True      
        
        return render(request, 'tube/library.html', context)

    else:
        return redirect('login')
    
    
def subscriptions(request):
    if request.user.is_authenticated:
        context = {}
        try:
            viewer = request.user.viewer
            context['viewer'] = viewer
            
            try:
                watchlater = Watchlater.objects.get(viewer=viewer)
                context['watchlater'] = watchlater

            except Watchlater.DoesNotExist:
                watchlater = Watchlater(viewer=viewer)
                watchlater.save()
                context['watchlater'] = watchlater

            try:
                subscription = Subscriptions.objects.get(viewer=viewer)

            except Subscriptions.DoesNotExist:
                subscription = Subscriptions(viewer=viewer)
                subscription.save()

            channels = subscription.subscriptions.all()
            videos = []

            for channel in channels:
                videos_dict = channel.video_set.filter(private=False, unlisted=False).in_bulk().values()
                for video in videos_dict:
                    videos.append(video)

            context['videos'] = videos
            context['channels'] = channels
            context['subscription'] = subscription

            try:
                nav_channel = Channel.objects.get(user=viewer)
                playlists = Playlist.objects.filter(channel=nav_channel) 
                context['playlists'] = playlists
                context['nav_channel'] = nav_channel
                context['channel'] = nav_channel
                context['no_channel'] = False
                context['many_channels'] = False

            except Channel.DoesNotExist:
                context['many_channels'] = False
                context['no_channel'] = True

            except:
                my_channels = Channel.objects.filter(user=viewer)
                my_playlists = []

                for channel in my_channels:
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values()
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True        
        return render(request, 'tube/subscriptions.html', context)

    else:
        return redirect('login')
    

def upload_video(request, pk):
    context = {}
    if request.user.is_authenticated:
        try:
            context['title'] = 'Upload Video'
            context['button'] = 'Upload'
            viewer = request.user.viewer
            context['viewer'] = viewer

            try:
                channel = Channel.objects.get(id=pk)

                if request.method == 'POST':
                    form = VideoForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save(channel=channel)
                        return redirect(f'/channel/{channel.id}') # type: ignore

                    else:
                        errors = check_errors(form)
                        context['errors'] = errors
                        form = VideoForm()
                        context['form'] = form

                else:
                    context['form'] = VideoForm()

            except Channel.DoesNotExist as e:
                return HttpResponseBadRequest(e, ", Have you created a channel")

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
             
        return render(request, 'tube/upload.html', context)

    else:
        return redirect('login')
    
    
def create_playlist(request, pk):
    context = {}
    if request.user.is_authenticated:
        try:
            context['title'] = 'Create Playlist'
            context['button'] = 'Create'
            viewer = request.user.viewer
            context['viewer'] = viewer

            try:
                channel = Channel.objects.get(id=pk) # type: ignore
                if request.method == 'POST':
                    form = PlaylistForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save(channel=channel)
                        return redirect(f'/channel/{channel.id}') # type: ignore

                    else:
                        errors = check_errors(form)
                        context['errors'] = errors 
                        form = PlaylistForm()
                        context['form'] = form

                else:
                    context['form'] = PlaylistForm()

            except Channel.DoesNotExist as e:
                return HttpResponseBadRequest(e, ", Have you created a channel")
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
             
        return render(request, 'tube/upload.html', context)

    else:
        return redirect('login')
    
    
##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################            AJAX FUNCTIONS         ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


def subscribe(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                pk = request.POST['channel_id']
                channel = Channel.objects.get(id=pk)
                viewer = request.user.viewer

                if channel.user == viewer: 
                    return JsonResponse({'success': False, 'error': 'You cannot subscribe to your own channel.'})

                else:
                    try:
                        subscriptions = Subscriptions.objects.get(viewer=viewer)

                    except Subscriptions.DoesNotExist:
                        subscriptions = Subscriptions(viewer=viewer)
                        subscriptions.save()
                    subscriptions.subscriptions.add(channel)
                    channel.subscribers.add(viewer) # type: ignore
                    subscriber_count = channel.subscribers.count() # type: ignore
                    return JsonResponse({'success': True, 'subscribed': True,'subscriber_count':subscriber_count})

            except Channel.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Channel does not exist.'})

        else:
            return HttpResponse('No POST in request')

    else:
        return redirect('login')
 
    
def unsubscribe(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                pk = request.POST['channel_id']
                channel = Channel.objects.get(id=pk)
                viewer = request.user.viewer

                if channel.user == viewer: 
                    return JsonResponse({'success': False, 'error': 'You cannot unsubscribe from your own channel.'})

                else:
                    try:
                        subscriptions = Subscriptions.objects.get(viewer=viewer)
                        subscriptions.subscriptions.remove(channel)

                    except Subscriptions.DoesNotExist:
                        subscriptions = Subscriptions(viewer=viewer)
                        subscriptions.save()
                    channel.subscribers.remove(viewer) # type: ignore
                    subscriber_count = channel.subscribers.count() # type: ignore
                    return JsonResponse({'success': True, 'unsubscribed': True,'subscriber_count': subscriber_count})

            except Channel.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Channel does not exist.'})

        else:
            return HttpResponse('No POST in request')

    else:
        return redirect('login')
   
    
def like(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                pk = request.POST['video_id']
                video = Video.objects.get(id=pk)
                viewer = request.user.viewer
                try:
                    liked_videos = LikedVideos.objects.get(viewer=viewer)

                except LikedVideos.DoesNotExist:
                    liked_videos = LikedVideos(viewer=viewer)
                    liked_videos.save()

                if liked_videos.videos.contains(video): 
                    return JsonResponse({'success':False})

                else:
                    video.likes += 1 # type: ignore
                    liked_videos.videos.add(video)
                    video.save()
                    return JsonResponse({'success': True, 'liked':True, 'likes_count': video.likes}) 

            except:
                return JsonResponse({'success':False})

        else:
            return HttpResponse('No POST in request')

    else:
        return redirect('login') 
  
    
def unlike(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                pk = request.POST['video_id']
                video = Video.objects.get(id=pk)
                viewer = request.user.viewer
                try:
                    liked_videos = LikedVideos.objects.get(viewer=viewer)
                    liked_videos.videos.remove(video)

                except LikedVideos.DoesNotExist:
                    liked_videos = LikedVideos(viewer=viewer)
                    liked_videos.save()
                    return JsonResponse({'success':False})

                except:
                    return JsonResponse({'success':False})
                    
                video.likes -= 1
                video.save()
                return JsonResponse({'success': True, 'liked':False, 'likes_count': video.likes}) 

            except:
                return JsonResponse({'success':False})

        else:
            return HttpResponse('No POST in request')

    else:
        return redirect('login') 
 
    
def dislike(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                pk = request.POST['video_id']
                video = Video.objects.get(id=pk)
                viewer = request.user.viewer

                try:
                    disliked_videos = DisLikedVideos.objects.get(viewer=viewer)

                except DisLikedVideos.DoesNotExist:
                    disliked_videos = DisLikedVideos(viewer=viewer)
                    disliked_videos.save()

                if disliked_videos.videos.contains(video): # type: ignore
                    return JsonResponse({'success':False})

                else:
                    video.dislikes += 1
                    disliked_videos.videos.add(video)
                    video.save()
                    return JsonResponse({'success': True, 'disliked':True, 'dislikes_count': video.dislikes}) 
            except:
                return JsonResponse({'success':False})

        else:
            return HttpResponse('No POST in request')

    else:
        return redirect('login') 
 
    
def undislike(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                pk = request.POST['video_id']
                video = Video.objects.get(id=pk)
                viewer = request.user.viewer

                try:
                    disliked_videos = DisLikedVideos.objects.get(viewer=viewer)
                    disliked_videos.videos.remove(video)

                except DisLikedVideos.DoesNotExist:
                    disliked_videos = DisLikedVideos(viewer=viewer)
                    disliked_videos.save()
                    return JsonResponse({'success':False})

                except:
                    return JsonResponse({'success':False})
                
                video.dislikes -= 1
                video.save()
                return JsonResponse({'success': True, 'disliked':False, 'dislikes_count': video.dislikes}) 

            except:
                return JsonResponse({'success':False})

        else:
            return HttpResponse('No POST in request')

    else:
        return redirect('login')
    

def add_view(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            pk = request.POST['video_id']
            video = Video.objects.get(id=pk)
            view = VideoView(viewer=viewer, video=video)
            view.save()
            
            try:
                history = History.objects.get(viewer=viewer)
                
            except:
                history = History(viewer=viewer)
                history.save()
                
            history.views.add(view)
            video.views += 1
            video.save()
            return JsonResponse({'success': True})
        else:
            return HttpResponse('No POST in request')
    else:
        if request.method=='POST':
            pk = request.POST['video_id']
            video = Video.objects.get(id=pk)
            view = VideoView(video=video)
            view.save()
            
            video.views += 1
            video.save()
            return JsonResponse({'success': True})
        else:
            return HttpResponse('No POST in request')
 

def add_video_to_playlist(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                video_id = request.POST['video_id']
                playlist_id = request.POST['playlist_id']
                video = Video.objects.get(id=video_id)
                playlist = Playlist.objects.get(id=playlist_id)
                playlist.videos.add(video)
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login') 
 

def remove_video_from_playlist(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                video_id = request.POST['video_id']
                playlist_id = request.POST['playlist_id']
                video = Video.objects.get(id=video_id)
                playlist = Playlist.objects.get(id=playlist_id)
                playlist.videos.remove(video)
                print('Here i am ##\t\t\t\t\t\n\t\t\t#########')
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login') 


def add_video_to_watchlater(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                video_id = request.POST['video_id']
                viewer = request.user.viewer
                video = Video.objects.get(id=video_id)
                watchlater = Watchlater.objects.get(viewer=viewer)
                watchlater.videos.add(video)
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')  


def remove_video_from_watchlater(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                video_id = request.POST['video_id']
                viewer = request.user.viewer
                video = Video.objects.get(id=video_id)
                watchlater = Watchlater.objects.get(viewer=viewer)
                watchlater.videos.remove(video)
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login') 
 
    
def save_playlist(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                playlist_pk = request.POST['playlist_id']
                viewer = request.user.viewer
                saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
                playlist = Playlist.objects.get(pk=playlist_pk)
                saved_playlists.playlists.add(playlist)
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
 
    
def unsave_playlist(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                playlist_pk = request.POST['playlist_id']
                viewer = request.user.viewer
                saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
                playlist = Playlist.objects.get(pk=playlist_pk)
                saved_playlists.playlists.remove(playlist)
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    
    
def delete_playlist(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            playlist_pk = request.POST['playlist_id']
            playlist = Playlist.objects.get(id=playlist_pk)
            
            if not playlist.channel.user == viewer: # type: ignore 
                return JsonResponse({'success':False, 'message':"You Don't own this Playlist"})
            try:
                playlist.delete()
                return JsonResponse({'success':True, 'message':"Playlist Deleted Successfully"})
            except:
                return JsonResponse({'success':False, 'message':"Deletion Failed"})
                
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    
    
def delete_video(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            video_pk = request.POST['video_id']
            video = Video.objects.get(id=video_pk)
            if not video.channel.user == viewer: # type: ignore 
                return JsonResponse({'success':False, 'message':"You Don't own this Video"})
            try:
                video.delete()
                return JsonResponse({'success':True, 'message':"Video Deleted Successfully"})
            except:
                return JsonResponse({'success':False, 'message':"Deletion Failed"})
                
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    

def comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                viewer = request.user.viewer
                video_id = request.POST['video_id']
                comment_text = request.POST['comment_text']
                video = Video.objects.get(id=video_id)
                channel = Channel.objects.get(user=viewer)
                comment = Comment(comment_text=comment_text, video=video, channel=channel)
                comment.save()
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    

def comment_many_channels(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                video_id = request.POST['video_id']
                comment_text = request.POST['comment_text']
                channel_id= request.POST['channel_id']
                video = Video.objects.get(id=video_id)
                channel = Channel.objects.get(id=channel_id)
                comment = Comment(comment_text=comment_text, video=video, channel=channel)
                comment.save()
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


def reply_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                viewer= request.user.viewer
                comment_id = request.POST['comment_id']
                reply_text = request.POST['reply_text']
                comment = Comment.objects.get(id=comment_id)
                channel = Channel.objects.get(user=viewer)
                comment_reply = CommentReply(comment=comment, reply=reply_text, channel=channel)
                comment_reply.save()
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')



def reply_comment_many_channels(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                channel_id = request.POST['channel_id']
                comment_id = request.POST['comment_id']
                reply_text = request.POST['reply_text']
                channel = Channel.objects.get(id=channel_id)
                comment = Comment.objects.get(id=comment_id)
                comment_reply = CommentReply(comment=comment, reply=reply_text, channel=channel)
                comment_reply.save()
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


def all_viewers(request):
    if request.user.is_authenticated:
        return render(request, 'tube/ajax_test.html')
    else:
        return redirect('login')
    
    
##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################         AJAX GET FUNCTIONS        ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


def get_viewers(request):
    viewers = Viewer.objects.all()
    return JsonResponse({'viewers':list(viewers.values())})


def get_subs(request, pk):
    channel = Channel.objects.get(id=pk)
    subscriber_count = channel.subscribers.count()
    return JsonResponse({"subscriber_count":subscriber_count})


def get_views(request, pk):
    video = Video.objects.get(id=pk)
    views = video.views
    return JsonResponse({"video_views":views})
