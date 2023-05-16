from django.contrib import admin
from .models import *


admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Playlist)
admin.site.register(Comment)
admin.site.register(CommentReply)


## COMMENT OUT LATER 
# Not suitable to be editable
admin.site.register(Viewer)
# admin.site.register(LikedVideos)
# admin.site.register(DisLikedVideos)
# admin.site.register(VideoView)
# admin.site.register(History)