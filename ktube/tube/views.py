from django.shortcuts import render
from .models import Video, Comment, CommentReply, Channel
from django.contrib.auth.models import User
from .filters import VideoFilter

# Create your views here.
def home_view(request):
    videos = Video.objects.all()
    
    myFilter = VideoFilter(request.GET, queryset=videos)
        
    context = {'videos': videos, 'myFilter': myFilter}
        
    if request.user.is_authenticated:
        # viewer = request.user.viewer
        # context['viewer'] = viewer
        pass
                
    return render(request, 'tube/home.html', context)


def watch_video(request, pk):
    video = Video.objects.get(id=pk)
    comments = Comment.objects.filter(video=video)
    comment_replies = CommentReply.objects.all()
    replies_dict = comment_replies.in_bulk()
    replies_list = []
    for key in range(len(replies_dict)):
        replies_list.append(replies_dict[key+1].reply) # strings
        
    
    context = {"video": video, "comments": comments, "comment_replies": comment_replies}
    return render(request, 'tube/watch.html', context)


def channnel_view(request, pk):
    channel = Channel.objects.get(id=pk)
    
    context = {'channel': channel}
    return render(request, 'tube/channel.html', context)
