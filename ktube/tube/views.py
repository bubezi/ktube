from django.shortcuts import render
from .models import Video, Viewer, Channel
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
    context = {"video": video}
    return render(request, 'tube/watch.html', context)
