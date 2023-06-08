from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import VideoForm, PlaylistForm
from register.utils import check_errors
from .filters import VideoFilter
from decimal import Decimal
from .models import *


PERCENTAGE_OF_REVENUE = Decimal('0.85')
COMPANY_USERNAME = 'bubezi'


##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################           VIEWS FUNCTIONS         ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


def home_view(request):
    context = {}
    videos = Video.objects.filter(private=False, unlisted=False) # type: ignore
    # myFilter = VideoFilter(request.GET, queryset=videos)
    # context['myFilter'] = myFilter
    context['videos'] = videos 
    context['title'] = "Home " 

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
                    channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values() # type: ignore
                    for channel_playlist in channel_playlists:
                        my_playlists.append(channel_playlist)
                context['playlists']= my_playlists
                context['my_channels']= my_channels
                context['many_channels'] = True
                context['no_channel'] = False

        except:
            context['no_channel'] = True       
    return render(request, 'tube/home.html', context)


def search_results_view(request):
    if request.method == 'POST':
        context = {}
        query = request.POST['searched']
        query = str(query)

        try:
            videos = Video.objects.filter(title__unaccent__lower__trigram_similar=query, private=False, unlisted=False) # type: ignore
        except:
            videos = Video.objects.filter(title__contains=query, private=False, unlisted=False) # type: ignore
        
            
        # name__unaccent__lower__trigram_similar
        # name__unaccent__icontains
        # name__contains
        # myFilter = VideoFilter(request.GET, queryset=videos)
        # context['myFilter'] = myFilter
        context['videos'] = videos 
        context['query'] = query
        context['title'] = f"{query} " 

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
                        channel_playlists = Playlist.objects.filter(channel=channel).in_bulk().values() # type: ignore
                        for channel_playlist in channel_playlists:
                            my_playlists.append(channel_playlist)
                    context['playlists']= my_playlists
                    context['my_channels']= my_channels
                    context['many_channels'] = True
                    context['no_channel'] = False

            except:
                context['no_channel'] = True
        return render(request, 'tube/search.html', context)
    else:
        return HttpResponse("No POST in request")      


def watch_video(request, pk):
    context = {}
    try:
        video = Video.objects.get(slug=pk) # type: ignore

    except Video.DoesNotExist:
        return HttpResponseBadRequest('<h1>404 Not Found</h1><h3>Video Does Not Exist! SORRYYY</h3>')   # type: ignore
    
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
    
    
    
    
    
    if video.price > 0:
        if request.user.is_authenticated:
            viewer = request.user.viewer
            if not video.channel.user == viewer:
                if not video.paid_viewers.contains(viewer):
                    if viewer.spend(video.price):
                        video_owner_cut = PERCENTAGE_OF_REVENUE * Decimal(video.price)
                        company_cut = Decimal(video.price) - video_owner_cut
                        video.channel.user.wallet += float(video_owner_cut)
                        main_viewer = Viewer.objects.get(username=COMPANY_USERNAME)
                        main_viewer.wallet += float(company_cut)
                        video.paid_viewers.add(viewer)
                        viewer.save()
                        main_viewer.save()
                        video.channel.user.save()
                        video.save()
                    else:
                        # return HttpResponse("<h1>Deposit money please</h1><h4>Your Video's owner wishes you would support their work</h4>")
                        return redirect('deposit')
        else:
            return redirect('login')  






    subscriber_count = video.channel.subscribers.count() # type: ignore
    comments = Comment.objects.filter(video=video)
    comment_replies = CommentReply.objects.all()
    
    paginator = Paginator(comments, 20) # 20 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # replies_dict = comment_replies.in_bulk()
    # replies_list = []
    # for key in range(len(replies_dict)):
    #     replies_list.append(replies_dict[key+1].reply) # replies here are strings
     
    context['video'] = video
    context['comments'] = page_obj
    context['comment_replies'] = comment_replies
    context['subscriber_count'] = subscriber_count
    
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
                playlists = Playlist.objects.filter(channel=nav_channel)  # type: ignore
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
    context = {}
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
        
    context['playlist'] = playlist
    
    videos = []
    if request.user.is_authenticated:
        viewer = request.user.viewer
        if playlist.channel.user == viewer: # type: ignore
            videos_dict = playlist.videos.all()
        else:
            videos_dict = playlist.videos.filter(private=False)
    else:
        videos_dict = playlist.videos.filter(private=False)
        
        
        #### The Patient Predator
    try:
        for video in videos_dict:
            videos.append(video)
        number = int(number)
        video = videos[number]

    except:
        return HttpResponseBadRequest('<h1>404 Not Found</h1><h3>Video Does Not Exist! SORRYYY</h3>')  
    
    
    context['video_number'] = number
    context['playlist_id'] = pk
    context['video_previous_exists'] = False
    
    if number!=0:
        context['video_previous'] = (number-1)
        context['video_previous_exists'] = True
    
    if number<len(videos)-1:
        context['video_next'] = number+1
        
    
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



    if video.price > 0:
        if request.user.is_authenticated:
            viewer = request.user.viewer
            if not video.channel.user == viewer:
                if not video.paid_viewers.contains(viewer):
                    if viewer.spend(video.price):
                        video_owner_cut = PERCENTAGE_OF_REVENUE * Decimal(video.price)
                        company_cut = Decimal(video.price) - video_owner_cut
                        video.channel.user.wallet += video_owner_cut
                        main_viewer = Viewer.objects.get(username=COMPANY_USERNAME)
                        main_viewer.wallet += company_cut
                        video.paid_viewers.add(viewer)
                        viewer.save()
                        main_viewer.save()
                        video.channel.user.save()
                        video.save()
                    else:
                        # return HttpResponse("<h1>Deposit money please</h1><h4>Your Video's owner wishes you would support their work</h4>")
                        return redirect('deposit')
        else:
            return redirect('login')  






    context['video'] = video

    subscriber_count = video.channel.subscribers.count() # type: ignore
    comments = Comment.objects.filter(video=video)
    comment_replies = CommentReply.objects.all()
    
    paginator = Paginator(comments, 10) # 10 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['comments'] = page_obj
    context['comment_replies'] = comment_replies
    context['subscriber_count'] = subscriber_count
    
    
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
    
    playlist.views += 1
    playlist.save()
    return render(request, 'tube/watch.html', context)


def channnel_view(request, pk):
    try:    
        channel = Channel.objects.get(id=pk)

    except Channel.DoesNotExist:
        return HttpResponse('<h1>404 Not Found</h1><h4>Channel Does Not Exist! SORRYYY</h4>')  
    
    if not channel.channel_active:
        return HttpResponse('<h1>404 Not Found</h1><h4>Channel Does Not Exist! SORRYYY</h4>')  
        
    videos = Video.objects.filter(channel=channel, unlisted=False, private=False)
    subscriber_count = channel.subscribers.count()
    playlists = Playlist.objects.filter(channel=channel, public=True) 
    context = {'channel': channel, "videos": videos, "subscriber_count": subscriber_count,
               'public_playlists': playlists} 
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
    
    
def edit_playlist_view(request, pk):
    if request.user.is_authenticated:
        viewer = request.user.viewer
        context = {}
        try:
            playlist = Playlist.objects.get(id=pk)
        except Playlist.DoesNotExist:
            return HttpResponseBadRequest('<h1>404 Not Found</h1><h3>Playlist Does Not Exist! SORRYYY</h3>')
        viewer = request.user.viewer
        if not viewer == playlist.channel.user:
            return JsonResponse({'success': False, 'message': "You don't own this Playlist"})
        context['playlist'] = playlist
                
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
        return render(request, 'tube/edit_playlist.html', context)
    else:
        return redirect('login')
    
    
def edit_video_view(request, pk):
    if request.user.is_authenticated:
        viewer = request.user.viewer
        context = {}
        try:
            video = Video.objects.get(slug=pk) # type: ignore
        except Video.DoesNotExist: # type: ignore
            return HttpResponseBadRequest('<h1>404 Not Found</h1><h3>Video Does Not Exist! SORRYYY</h3>')
        if not viewer == video.channel.user: # type: ignore
            return JsonResponse({'success': False, 'message': "You don't own this Video"})
        context['video'] = video
                
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
        return render(request, 'tube/edit_video.html', context)
    else:
        return redirect('login')


def my_channels_page(request):        
    if request.user.is_authenticated:
        viewer = request.user.viewer
        try:
            watchlater = Watchlater.objects.get(viewer=viewer)
        except Watchlater.DoesNotExist:
            watchlater = Watchlater(viewer=viewer)
            watchlater.save()
        context={'viewer': viewer, 'many_channels': False, "watchlater" : watchlater}
        try:
            channel = Channel.objects.get(user=viewer)
            context['channel']=channel
            context['nav_channel']=channel
            context['many_channels'] = False
            context['no_channel'] = False
        except Channel.DoesNotExist:
            context['many_channels'] = False
            context['no_channel'] = True
        except:
            context['many_channels'] = True
            context['no_channel'] = False
            
        if context['many_channels']:
            my_channels = Channel.objects.filter(user=viewer)
            context['my_channels'] = my_channels
        return render(request, "tube/my_channels.html", context)
    else:
        return redirect('login')


def deposit_view(request):
    context = {}
    if request.user.is_authenticated:
        viewer = request.user.viewer
        context['viewer'] = viewer
        try:
            channel = Channel.objects.get(user=viewer)
            context['channel']=channel
            context['nav_channel']=channel
            context['many_channels'] = False
            context['no_channel'] = False
        except Channel.DoesNotExist:
            context['many_channels'] = False
            context['no_channel'] = True
        except:
            context['many_channels'] = True
            context['no_channel'] = False
            
        if context['many_channels']:
            my_channels = Channel.objects.filter(user=viewer)
            context['my_channels'] = my_channels
        return render(request, "tube/deposit.html", context)
    else:
        return redirect('login')
    
    
##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################            AJAX FUNCTIONS         ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


def deposit_funds(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                ammount = request.POST['ammount']
                viewer = request.user.viewer
                viewer.wallet += float(ammount)
                viewer.save()

                return JsonResponse({'success': True, 'message': 'Deposit Successfull'})
            except:
                return JsonResponse({'success': False, 'message': 'Error Depositing'})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


def edit_playlist(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pk = request.POST['playlist_id']
            try:
                playlist = Playlist.objects.get(id=pk)
            except Playlist.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Playlist Does Not Exist"})
            viewer = request.user.viewer
            if not viewer == playlist.channel.user:
                return JsonResponse({'success': False, 'message': "You don't own this Playlist"})
            try:
                try:
                    name = request.POST['playlist_name']
                    if name =="":
                        name = playlist.name
                except:
                    name = playlist.name
                try:
                    public = request.POST['playlist_public']
                    if public=="true":
                        public = True
                    else:
                        public = False
                except:
                    public = playlist.public
                playlist.name = name
                playlist.public = public
                playlist.save()
                return JsonResponse({'success': True, 'message': "Saved", 'name': playlist.name, 'public': playlist.public})
            except:
                return JsonResponse({'success': False, 'message': "ERROR saving data"})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


def edit_video(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pk = request.POST['video_id']
            try:
                video = Video.objects.get(slug=pk)
            except Video.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Video Does Not Exist"})
            viewer = request.user.viewer
            if not viewer == video.channel.user: # type: ignore
                return JsonResponse({'success': False, 'message': "You don't own this Video"})
            try:
                if not request.POST['video_title'] == "":
                    video_title = request.POST['video_title']
                else:
                    video_title = video.title
                try:
                    if request.POST['video_private'] == 'true':
                        video_private = True
                    else:
                        video_private = False
                except:
                    video_private = video.private
                try:
                    if request.POST['video_unlisted'] == 'true':
                        video_unlisted = True
                    else:
                        video_unlisted = False
                except:
                    video_unlisted = video.unlisted
                if not request.POST['video_thumbnail'] == "":
                    video_thumbnail = request.POST['video_thumbnail']
                else:
                    video_thumbnail = video.thumbnail
                if not request.POST['video_description'] == "":
                    video_description = request.POST['video_description']
                else:
                    video_description = video.description
                if not request.POST['video_price'] == "":
                    video_price = request.POST['video_price']
                else:
                    video_price = video.price
                video.title = video_title
                video.private = video_private
                video.unlisted = video_unlisted
                video.thumbnail = video_thumbnail
                video.description = video_description
                video.price = video_price
                video.save()
                return JsonResponse({'success': True, 'message': "Saved"})
            except:
                return JsonResponse({'success': False, 'message': "ERROR saving data"})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


# def edit_video(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             pk = request.POST['video_id']
#             try:
#                 video = Video.objects.get(slug=pk)
#             except Video.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': "Video Does Not Exist"})
#             viewer = request.user.viewer
#             if not viewer == video.channel.user: # type: ignore
#                 return JsonResponse({'success': False, 'message': "You don't own this Video"})
#             try:
#                 return JsonResponse({'success': True, 'message': "Saved"})
#             except:
#                 return JsonResponse({'success': False, 'message': "ERROR saving data"})
#         else:
#             return HttpResponse('No POST in request')
#     else:
#         return redirect('login')


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
                video = Video.objects.get(slug=pk)
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
                video = Video.objects.get(slug=pk)
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
                video = Video.objects.get(slug=pk)
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
                video = Video.objects.get(slug=pk)
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
    from .utils import view_valid
    
    
    INVALID_MINUTES = 5
    
    
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            pk = request.POST['video_id']
            video = Video.objects.get(slug=pk)
            view = VideoView(viewer=viewer, video=video)
            view.save()
            
            try:
                history = History.objects.get(viewer=viewer)
                
            except:
                history = History(viewer=viewer)
                history.save()
                
            history.views.add(view)
            
            # The python approach, lie there and wait
            previous_view = 0
            previous_views = video.videoview_set.order_by('viewed_on').filter(viewer=viewer).reverse().in_bulk().values() # type: ignore
            if len(previous_views)>1:
                for index, v in enumerate(previous_views):
                    previous_view = v
                    if index == 1:
                        break
                if view_valid(previous_view, INVALID_MINUTES):   
                    video.views += 1
                    video.save()
            else:
                video.views += 1
                video.save()
            return JsonResponse({'success': True})
        else:
            return HttpResponse('No POST in request')
    else:
        if request.method=='POST':
            pk = request.POST['video_id']
            video = Video.objects.get(slug=pk)
            view = VideoView(video=video)
            view.save()
            video.save()
            
            previous_view=0
            # previous_views = video.videoview_set.order_by('viewed_on').filter(viewer=viewer).reverse().in_bulk().values() # type: ignore
            if len(previous_views)>1:
                for index, v in enumerate(previous_views):
                    previous_view = v
                    if index == 1:
                        break
                    
                if view_valid(previous_view, INVALID_MINUTES): 
                    video.views += 1
                    video.save()
            else:
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
                video = Video.objects.get(slug=video_id)
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
                video = Video.objects.get(slug=video_id)
                playlist = Playlist.objects.get(id=playlist_id)
                playlist.videos.remove(video)
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
                video = Video.objects.get(slug=video_id)
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
                video = Video.objects.get(slug=video_id)
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
            video = Video.objects.get(slug=video_pk)
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
    
    
def delete_channel(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            channel_pk = request.POST['channel_id']
            channel = Channel.objects.get(id=channel_pk)
            if not channel.user == viewer: # type: ignore 
                return JsonResponse({'success':False, 'message':"You Don't own this Channel"})
            try:
                channel.delete()
                return JsonResponse({'success':True, 'message':"Channel Deleted Successfully"})
            except:
                return JsonResponse({'success':False, 'message':"Deletion Failed"})
                
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    
    
def delete_comment_reply(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            comment_reply_pk = request.POST['comment_reply_id']
            comment_reply = CommentReply.objects.get(id=comment_reply_pk)
            if not comment_reply.channel.user == viewer: # type: ignore 
                return JsonResponse({'success':False, 'message':"You Don't own this Comment reply"})
            try:
                comment_reply.delete()
                return JsonResponse({'success':True, 'message':"Comment reply Deleted Successfully"})
            except:
                return JsonResponse({'success':False, 'message':"Deletion Failed"})
                
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    
    
def delete_comment(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viewer = request.user.viewer
            comment_pk = request.POST['comment_id']
            comment = Comment.objects.get(id=comment_pk)
            if not comment.channel.user == viewer: # type: ignore 
                return JsonResponse({'success':False, 'message':"You Don't own this Comment"})
            try:
                comment.delete()
                return JsonResponse({'success':True, 'message':"Comment Deleted Successfully"})
            except:
                return JsonResponse({'success':False, 'message':"Deletion Failed"})
                
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')
    
    
def delete_account(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            try:
                user = request.user
                viewer = user.viewer
                channnels = Channel.objects.filter(user=viewer)
                try:
                    viewer.subscriptions.subscriptions.clear()
                except:
                    pass
                for channel in channnels:
                    channel.channel_active = False
                    channel.subscribers.clear()
                    channel_videos = channel.video_set.in_bulk().values() # type: ignore
                    channel_playlists = channel.playlist_set.in_bulk().values() # type: ignore
                    subscriptions_to_channel = channel.subscriptions.in_bulk().values() # type: ignore
                    for subscription in subscriptions_to_channel:
                        subscription.subscriptions.remove(channel)
                    for video in channel_videos:
                        video_playlists = video.playlists.all()
                        video_comments = video.comment_set.in_bulk().values()
                        for video_playlist in video_playlists:
                            video_playlist.videos.remove(video)
                        for comment in video_comments:
                            comment.delete()
                        video.private = True
                        video.save()
                    for playlist in channel_playlists:
                        playlist.delete()
                    channel.save()
                user.is_active = False
                user.save()
                
                #### or comment the above block and comment out the following
                # user.delete()
                return JsonResponse({'success':True, 'message':"Account Deleted Successfully"})
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
                if len(comment_text) < 3:
                    return JsonResponse({'success': False})
                video = Video.objects.get(slug=video_id)
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
                if len(comment_text) < 3:
                    return JsonResponse({'success': False})
                channel_id= request.POST['channel_id']
                video = Video.objects.get(slug=video_id)
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
                if len(reply_text) < 3:
                    return JsonResponse({'success': False})
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
                if len(reply_text) < 3:
                    return JsonResponse({'success': False})
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


from django.contrib.auth import authenticate


def authenticate_action(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            username = user.username
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                return JsonResponse({'success':True})
            else:
                return JsonResponse({'success':False, 'message':"Wrong Password"})
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


def like_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            viewer = request.user.viewer
            comment_id = request.POST['comment_id']
            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Comment Does not Exist"})
            try:
                liked_comments = LikedComments.objects.get(viewer=viewer)
            except:
                liked_comments = LikedComments(viewer=viewer)
                liked_comments.save()
            
            if liked_comments.comments.contains(viewer):
                return JsonResponse({'success':False, 'message':'Comment already liked'})
            
            liked_comments.comments.add(comment)
            comment.likes += 1
            comment.save()
            return JsonResponse({'success':True, 'likes': comment.likes}) 
        else:
            return HttpResponse('No POST in request')
    else:
        return redirect('login')


def dislike_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            viewer = request.user.viewer
            comment_id = request.POST['comment_id']
            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Comment Does not Exist"})
            try:
                disliked_comments = DisLikedComments.objects.get(viewer=viewer)
            except:
                disliked_comments = DisLikedComments(viewer=viewer)
                disliked_comments.save()
            
            if disliked_comments.comments.contains(viewer):
                return JsonResponse({'success':False, 'message':'Comment already disliked'})
            
            disliked_comments.comments.add(comment)
            comment.dislikes += 1
            comment.save()
            return JsonResponse({'success':True, 'dislikes': comment.dislikes}) 
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
    video = Video.objects.get(slug=pk)
    views = video.views
    return JsonResponse({"video_views":views})
