from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Viewer)
admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Playlist)
admin.site.register(Comment)
admin.site.register(CommentReply)
