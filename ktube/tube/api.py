from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .forms import VideoForm, PlaylistForm
from register.utils import check_errors
from django.utils import timezone
from .filters import VideoFilter
from decimal import Decimal
from .models import *


##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################               SETTINGS            ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


PERCENTAGE_OF_REVENUE = Decimal("0.85")
COMPANY_USERNAME = "bubezi"


##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################             API FUNCTIONS         ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################

from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied


class WatchlaterHomeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = request.user.viewer

        try:
            watchlater = Watchlater.objects.get(viewer=viewer)

        except Watchlater.DoesNotExist:
            watchlater = Watchlater(viewer=viewer)
            watchlater.save()

        serializer = WatchlaterSerializer(watchlater, many=False)
        return Response({"watchlater": serializer.data}, status=status.HTTP_200_OK)


class WatchlaterVideosAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = request.user.viewer
        try:
            watchlater = Watchlater.objects.get(viewer=viewer)
            videos = watchlater.videos
            serializer = VideoSerializer(videos, many=True)
            return Response({"watchlater": serializer.data}, status=status.HTTP_200_OK)

        except Watchlater.DoesNotExist:
            watchlater = Watchlater(viewer=viewer)
            watchlater.save()
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )


class SavedPlaylistsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = request.user.viewer
        try:
            savedPlaylists = SavedPlaylists.objects.get(viewer=viewer)
        except SavedPlaylists.DoesNotExist:
            savedPlaylists = SavedPlaylists(viewer=viewer)
            savedPlaylists.save()
        serializer = SavedPlaylists_Serializer(savedPlaylists, many=False)
        return Response({"savedPlaylists": serializer.data}, status=status.HTTP_200_OK)


class SavedPlaylists2API(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = request.user.viewer
        try:
            saved_playlists = SavedPlaylists.objects.get(viewer=viewer).playlists.all()
            serializer = PlaylistSerializer(saved_playlists, many=True)
            return Response(
                {"savedPlaylists": serializer.data}, status=status.HTTP_200_OK
            )
        except SavedPlaylists.DoesNotExist:
            savedPlaylists = SavedPlaylists(viewer=viewer)
            savedPlaylists.save()
            return Response(
                {"error": "Playlists Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )


class MyPlaylistsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewer = request.user.viewer
        my_playlists = Playlist.objects.filter(channel__user=viewer)
        serializer = PlaylistSerializer(my_playlists, many=True)
        return Response({"myPlaylists": serializer.data}, status=status.HTTP_200_OK)


class MyLikedVideosAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = LikedVideos.objects.get(viewer=request.user.viewer).videos
        serializer = VideoSerializer(videos, many=True)
        return Response({"MyLikedVideos": serializer.data}, status=status.HTTP_200_OK)


class MyHistoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        views = History.objects.get(viewer=request.user.viewer).views.order_by("viewed_on").reverse()
        new_views = []
        for index, v in enumerate(views):
            if index == 0:
                new_views.append(v)
            else:
                if not new_views[-1].video == v.video:
                    new_views.append(v)
                        
        videos = []    
        for view in new_views:
            videos.append(view.video)
        serializer = VideoSerializer(videos, many=True)
        # serializer = VideoViewSerializer(new_views)
        return Response({"MyHistory": serializer.data}, status=status.HTTP_200_OK)


class PlaylistsHomeAPI(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        viewer = request.user.viewer

        playlists = []

        try:
            playlists = Playlist.objects.filter(channel__user=viewer)

        except Channel.DoesNotExist:
            pass

        except:
            my_channels = Channel.objects.filter(user=viewer)
            playlists = []

            for channel in my_channels:
                channel_playlists = Playlist.objects.filter(channel=channel)
                playlists.extend(channel_playlists)

        serializer = PlaylistsHomeSerializer(playlists, many=True)
        return Response({"playlists": serializer.data}, status=status.HTTP_200_OK)


class VideosHome(generics.ListAPIView):
    queryset = Video.objects.filter(private=False, unlisted=False)
    serializer_class = VideosHomeSerializer


class ChannelProfilePicture(generics.RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelProfilePictureSerializer


class Watch_video_API(APIView):
    def get(self, request, slug, format=None):
        try:
            video = Video.objects.get(slug=slug)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        # If the video is private, make sure the viewer is the owner
        if video.private:
            if request.user.is_authenticated:
                try:
                    viewer = request.user.viewer
                    if not video.channel.user == viewer:
                        raise PermissionDenied("You are not the owner of this video")
                except Viewer.DoesNotExist:
                    raise PermissionDenied("You are not the owner of this video")

        # Handle monetisation
        if video.price > 0:
            if request.user.is_authenticated:
                viewer = request.user.viewer
                if not video.channel.user == viewer:
                    if not video.paid_viewers.contains(viewer):
                        if viewer.spend(video.price):
                            video_owner_cut = PERCENTAGE_OF_REVENUE * Decimal(
                                video.price
                            )
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
                            return Response(
                                {"error": "Please deposit money to watch this video"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
            else:
                raise PermissionDenied("You are not logged in")

        # Serialize video
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Watch_playlist_API(APIView):
    def get(self, request, id, format=None):
        try:
            video = Video.objects.get(id=id)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        # If the video is private, make sure the viewer is the owner
        if video.private:
            if request.user.is_authenticated:
                try:
                    viewer = request.user.viewer
                    if not video.channel.user == viewer:
                        raise PermissionDenied("You are not the owner of this video")
                except Viewer.DoesNotExist:
                    raise PermissionDenied("You are not the owner of this video")

        # Handle monetisation
        if video.price > 0:
            if request.user.is_authenticated:
                viewer = request.user.viewer
                if not video.channel.user == viewer:
                    if not video.paid_viewers.contains(viewer):
                        if viewer.spend(video.price):
                            video_owner_cut = PERCENTAGE_OF_REVENUE * Decimal(
                                video.price
                            )
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
                            return Response(
                                {"error": "Please deposit money to watch this video"},
                                status=status.HTTP_403_FORBIDDEN,
                            )
            else:
                raise PermissionDenied("You are not logged in")

        # Serialize video
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Channel_API(APIView):
    def get(self, request, id, format=None):
        try:
            channel = Channel.objects.get(id=id)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Get_Channels_API(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        viewer = Viewer.objects.get(id=id)

        channels = []

        try:
            my_channels = Channel.objects.filter(user=viewer)

            if not my_channels:
                return Response(
                    {"error": "No Channels Found!"}, status=status.HTTP_404_NOT_FOUND
                )

            if len(my_channels) == 1:
                channels.append(my_channels[0])
            else:
                channels.extend(my_channels)

        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = ChannelSerializer(channels, many=True)
        return Response({"channels": serializer.data}, status=status.HTTP_200_OK)


class Is_owner_API(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        viewer_signed_in = request.user.viewer
        try:
            channel = Channel.objects.get(id=id)
            viewer_in_db = channel.user
        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        owner = viewer_signed_in == viewer_in_db

        return Response({"is_owner": owner}, status=status.HTTP_200_OK)


class Is_playlist_owner_API(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        viewer_signed_in = request.user.viewer
        try:
            playlist = Playlist.objects.get(id=id)
            viewer_in_db = playlist.channel.user
        except Playlist.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        owner = viewer_signed_in == viewer_in_db

        return Response({"is_owner": owner}, status=status.HTTP_200_OK)


class Get_comments_API(APIView):
    def get(self, request, id, format=None):
        try:
            video = Video.objects.get(id=id)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            comments = Comment.objects.filter(video=video)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Get_replies_API(APIView):
    def get(self, request, id, format=None):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            comment_replies = CommentReply.objects.filter(comment=comment)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentReplySerializer(comment_replies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Liked_API(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        viewer = request.user.viewer
        try:
            video = Video.objects.get(id=id)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            liked_videos = LikedVideos.objects.get(viewer=viewer)
        except LikedVideos.DoesNotExist:
            return Response(
                {"error": "LikedVideos Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        liked = liked_videos.videos.contains(video)

        return Response({"liked": liked}, status=status.HTTP_200_OK)


class DisLiked_API(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        viewer = request.user.viewer
        try:
            video = Video.objects.get(id=id)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            disliked_videos = DisLikedVideos.objects.get(viewer=viewer)
        except DisLikedVideos.DoesNotExist:
            return Response(
                {"error": "DisLikedVideos Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

        disliked = disliked_videos.videos.contains(video)

        return Response({"disliked": disliked}, status=status.HTTP_200_OK)


class More_Videos_API(APIView):
    def get(self, request, id, format=None):
        try:
            more_videos = (
                Video.objects.exclude(id=id)
                .exclude(private=True)
                .exclude(unlisted=True)
            )

        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(more_videos, many=True)

        return Response({"videos": serializer.data}, status.HTTP_200_OK)


class More_Playlist_Videos_API(APIView):
    def get(self, request, playlistId, videoId, format=None):
        try:
            playlist = Playlist.objects.get(id=playlistId)

            more_videos = playlist.videos
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(more_videos, many=True)

        return Response({"videos": serializer.data}, status.HTTP_200_OK)


class PlaylistAPI(APIView):
    def get(self, request, playlistId):
        try:
            playlist = Playlist.objects.get(id=playlistId)
            if playlist.public:
                serializer = PlaylistSerializer(playlist, many=False)
                return Response(serializer.data, status.HTTP_200_OK)
            elif request.user.viewer == playlist.channel.user:
                serializer = PlaylistSerializer(playlist, many=False)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Playlist Not public!"}, status=status.HTTP_403_FORBIDDEN
                )
        except Playlist.DoesNotExist:
            return Response(
                {"error": "Playlist Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
            )


class PlaylistVideosAPI(APIView):
    def get(self, request, playlistId):
        try:
            videos = Playlist.objects.get(id=playlistId).videos
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Playlist.DoesNotExist:
            return Response(
                {"error": "Playlist Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except Video.DoesNotExist:
            return Response(
                {"error": "Video Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChannelVideos(APIView):
    def get(self, request, channelId):
        try:
            channel = Channel.objects.get(id=channelId)
            videos = Video.objects.filter(
                channel=channel, private=False, unlisted=False
            )
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChannelUnlistedVideos(APIView):
    def get(self, request, channelId):
        try:
            channel = Channel.objects.get(id=channelId)
            videos = Video.objects.filter(channel=channel, unlisted=True)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChannelPrivateVideos(APIView):
    def get(self, request, channelId):
        try:
            channel = Channel.objects.get(id=channelId)
            videos = Video.objects.filter(channel=channel, private=True)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChannelPlaylists(APIView):
    def get(self, request, channelId):
        try:
            channel = Channel.objects.get(id=channelId)
            playlists = Playlist.objects.filter(channel=channel)
            serializer = PlaylistsHomeSerializer(playlists, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Channel Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
def add_video_to_playlist_API(request):
    video_id = request.data.get("video_id")
    playlist_id = request.data.get("playlist_id")

    if video_id is None or playlist_id is None:
        return Response(
            {"error": "video_id and playlist_id are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        video = Video.objects.get(id=video_id)
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.videos.add(video)
        return Response(status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Playlist.DoesNotExist:
        return Response(
            {"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def remove_video_from_playlist_API(request):
    video_id = request.data.get("video_id")
    playlist_id = request.data.get("playlist_id")

    if video_id is None or playlist_id is None:
        return Response(
            {"error": "video_id and playlist_id are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        video = Video.objects.get(id=video_id)
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.videos.remove(video)
        return Response(status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Playlist.DoesNotExist:
        return Response(
            {"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            {"error": "Some other error"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def add_video_to_watchlater_API(request):
    video_id = request.data.get("video_id")

    if video_id is None:
        return Response(
            {"error": "video_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        viewer = request.user.viewer
        video = Video.objects.get(id=video_id)
        watchlater = Watchlater.objects.get(viewer=viewer)
        watchlater.videos.add(video)
        return Response(status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Playlist.DoesNotExist:
        return Response(
            {"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def remove_video_from_watchlater_API(request):
    video_id = request.data.get("video_id")

    if video_id is None:
        return Response(
            {"error": "video_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        viewer = request.user.viewer
        video = Video.objects.get(id=video_id)
        watchlater = Watchlater.objects.get(viewer=viewer)
        watchlater.videos.remove(video)
        return Response(status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Playlist.DoesNotExist:
        return Response(
            {"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_comment_API(request):
    comment_id = request.data.get("comment_id")

    if comment_id is None:
        return Response(
            {"error": "comment_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        viewer = request.user.viewer
        comment = Comment.objects.get(id=comment_id)
        if not comment.channel.user == viewer:  # type: ignore
            return Response(
                {"success": False, "message": "You Don't own this Comment"},
                status=status.HTTP_404_BAD_REQUEST,
            )
        try:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(
                {"success": False, "message": "Deletion Failed"},
                status=status.HTTP_404_BAD_REQUEST,
            )
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_reply_API(request):
    reply_id = request.data.get("reply_id")

    if reply_id is None:
        return Response(
            {"error": "reply_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        viewer = request.user.viewer
        reply = CommentReply.objects.get(id=reply_id)
        if not reply.channel.user == viewer:  # type: ignore
            return Response(
                {"success": False, "message": "You Don't own this Reply"},
                status=status.HTTP_404_BAD_REQUEST,
            )
        try:
            reply.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(
                {"success": False, "message": "Deletion Failed"},
                status=status.HTTP_404_BAD_REQUEST,
            )
    except CommentReply.DoesNotExist:
        return Response(
            {"error": "CommentReply not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def subscribe_API(request):
    try:
        channel_id = request.data.get("channel_id")
        viewer_id = request.data.get("viewer_id")
        channel = Channel.objects.get(id=channel_id)
        viewer = Viewer.objects.get(id=viewer_id)

        if channel.user == viewer:
            return Response(
                {
                    "success": False,
                    "message": "You cannot subscribe to your own channel.",
                },
                status=status.HTTP_404_BAD_REQUEST,
            )

        try:
            subscriptions = Subscriptions.objects.get(viewer=viewer)
        except Subscriptions.DoesNotExist:
            subscriptions = Subscriptions(viewer=viewer)
            subscriptions.save()

        subscriptions.subscriptions.add(channel)
        channel.subscribers.add(viewer)  # type: ignore
        return Response(status=status.HTTP_200_OK)
    except Channel.DoesNotExist:
        return Response(
            {"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def unsubscribe_API(request):
    try:
        channel_id = request.data.get("channel_id")
        viewer_id = request.data.get("viewer_id")
        channel = Channel.objects.get(id=channel_id)
        viewer = Viewer.objects.get(id=viewer_id)

        if channel.user == viewer:
            return Response(
                {
                    "success": False,
                    "message": "You cannot unsubscribe to your own channel.",
                },
                status=status.HTTP_404_BAD_REQUEST,
            )

        try:
            subscriptions = Subscriptions.objects.get(viewer=viewer)
            subscriptions.subscriptions.remove(channel)
        except Subscriptions.DoesNotExist:
            subscriptions = Subscriptions(viewer=viewer)
            subscriptions.save()

        channel.subscribers.remove(viewer)  # type: ignore
        return Response(status=status.HTTP_200_OK)
    except Channel.DoesNotExist:
        return Response(
            {"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def save_playlist_API(request):
    try:
        playlist_id = request.data.get("playlist_id")
        viewer_id = request.data.get("viewer_id")
        playlist = Playlist.objects.get(id=playlist_id)
        viewer = Viewer.objects.get(id=viewer_id)
        try:
            saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
        except SavedPlaylists.DoesNotExist:
            saved_playlists = SavedPlaylists(viewer=viewer)
            saved_playlists.save()

        saved_playlists.playlists.add(playlist)
        return Response(status=status.HTTP_200_OK)
    except Playlist.DoesNotExist:
        return Response(
            {"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def un_save_playlist_API(request):
    try:
        playlist_id = request.data.get("playlist_id")
        viewer_id = request.data.get("viewer_id")
        playlist = Playlist.objects.get(id=playlist_id)
        viewer = Viewer.objects.get(id=viewer_id)
        try:
            saved_playlists = SavedPlaylists.objects.get(viewer=viewer)
            saved_playlists.playlists.remove(playlist)
        except SavedPlaylists.DoesNotExist:
            saved_playlists = SavedPlaylists(viewer=viewer)
            saved_playlists.save()

        return Response(status=status.HTTP_200_OK)
    except Playlist.DoesNotExist:
        return Response(
            {"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def comment_API(request):
    try:
        video_id = request.POST.get("video_id")
        comment_text = request.POST.get("comment_text")
        viewer = request.user.viewer
        if len(comment_text) < 3:
            return JsonResponse({"success": False})
        video = Video.objects.get(id=video_id)
        channel = Channel.objects.get(user=viewer)
        comment = Comment(comment_text=comment_text, video=video, channel=channel)
        comment.save()
        return Response(status=status.HTTP_201_CREATED)
    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Channel.DoesNotExist:
        return Response(
            {"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def comment_many_channels_API(request):
    try:
        video_id = request.POST.get("video_id")
        comment_text = request.POST.get("comment_text")
        channel_id = request.POST.get("channel_id")
        if len(comment_text) < 3:
            return JsonResponse({"success": False})
        video = Video.objects.get(id=video_id)
        channel = Channel.objects.get(id=channel_id)
        comment = Comment(comment_text=comment_text, video=video, channel=channel)
        comment.save()
        return Response(status=status.HTTP_201_CREATED)
    except Channel.DoesNotExist:
        return Response(
            {"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def reply_API(request):
    try:
        comment_id = request.POST.get("comment_id")
        reply_text = request.POST.get("reply_text")
        viewer = request.user.viewer
        if len(reply_text) < 3:
            return JsonResponse({"success": False})
        comment = Comment.objects.get(id=comment_id)
        channel = Channel.objects.get(user=viewer)
        reply = CommentReply(reply=reply_text, comment=comment, channel=channel)
        reply.save()
        return Response(status=status.HTTP_201_CREATED)
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Channel.DoesNotExist:
        return Response(
            {"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def reply_many_channels_API(request):
    try:
        comment_id = request.POST.get("comment_id")
        reply_text = request.POST.get("reply_text")
        channel_id = request.POST.get("channel_id")
        if len(reply_text) < 3:
            return JsonResponse({"success": False})
        comment = Comment.objects.get(id=comment_id)
        channel = Channel.objects.get(id=channel_id)
        reply = CommentReply(reply=reply_text, comment=comment, channel=channel)
        reply.save()
        return Response(status=status.HTTP_201_CREATED)
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Channel.DoesNotExist:
        return Response(
            {"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def like_API(request):
    try:
        video_id = request.data.get("video_id")
        viewer_id = request.data.get("viewer_id")
        video = Video.objects.get(id=video_id)
        viewer = Viewer.objects.get(id=viewer_id)
        try:
            liked_videos = LikedVideos.objects.get(viewer=viewer)

        except LikedVideos.DoesNotExist:
            liked_videos = LikedVideos(viewer=viewer)
            liked_videos.save()

        if liked_videos.videos.contains(video):
            return Response(
                {"error": "Video already liked"}, status=status.HTTP_404_BAD_REQUEST
            )

        else:
            video.likes += 1  # type: ignore
            liked_videos.videos.add(video)
            video.save()
            return Response(status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except LikedVideos.DoesNotExist:
        return Response(
            {"error": "LikedVideos not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Viewer.DoesNotExist:
        return Response({"error": "Viewer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def dislike_API(request):
    try:
        video_id = request.data.get("video_id")
        viewer_id = request.data.get("viewer_id")
        video = Video.objects.get(id=video_id)
        viewer = Viewer.objects.get(id=viewer_id)
        try:
            disliked_videos = DisLikedVideos.objects.get(viewer=viewer)

        except DisLikedVideos.DoesNotExist:
            disliked_videos = DisLikedVideos(viewer=viewer)
            disliked_videos.save()

        if disliked_videos.videos.contains(video):
            return Response(
                {"error": "Video already disliked"}, status=status.HTTP_404_BAD_REQUEST
            )

        else:
            video.dislikes += 1  # type: ignore
            disliked_videos.videos.add(video)
            video.save()
            return Response(status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except DisLikedVideos.DoesNotExist:
        return Response(
            {"error": "DisLikedVideos not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Viewer.DoesNotExist:
        return Response({"error": "Viewer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def unlike_API(request):
    try:
        video_id = request.data.get("video_id")
        viewer_id = request.data.get("viewer_id")
        video = Video.objects.get(id=video_id)
        viewer = Viewer.objects.get(id=viewer_id)
        try:
            liked_videos = LikedVideos.objects.get(viewer=viewer)

            if liked_videos.videos.contains(video):
                video.likes -= 1  # type: ignore
                liked_videos.videos.remove(video)
                video.save()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response(
                    {"error": "Video already unliked"},
                    status=status.HTTP_404_BAD_REQUEST,
                )

        except LikedVideos.DoesNotExist:
            liked_videos = LikedVideos(viewer=viewer)
            liked_videos.save()

    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except LikedVideos.DoesNotExist:
        return Response(
            {"error": "LikedVideos not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Viewer.DoesNotExist:
        return Response({"error": "Viewer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def undislike_API(request):
    try:
        video_id = request.data.get("video_id")
        viewer_id = request.data.get("viewer_id")
        video = Video.objects.get(id=video_id)
        viewer = Viewer.objects.get(id=viewer_id)
        try:
            disliked_videos = DisLikedVideos.objects.get(viewer=viewer)

            if disliked_videos.videos.contains(video):
                video.dislikes -= 1  # type: ignore
                disliked_videos.videos.remove(video)
                video.save()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response(
                    {"error": "Video already undisliked"},
                    status=status.HTTP_404_BAD_REQUEST,
                )

        except DisLikedVideos.DoesNotExist:
            disliked_videos = DisLikedVideos(viewer=viewer)
            disliked_videos.save()

        if disliked_videos.videos.contains(video):
            return Response(
                {"error": "Video already disliked"}, status=status.HTTP_404_BAD_REQUEST
            )

        else:
            video.dislikes += 1  # type: ignore
            disliked_videos.videos.add(video)
            video.save()
            return Response(status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except DisLikedVideos.DoesNotExist:
        return Response(
            {"error": "DisLikedVideos not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Viewer.DoesNotExist:
        return Response({"error": "Viewer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_view_API(request):
    from .utils import view_valid

    INVALID_MINUTES = 5
    viewer_ip = request.META.get("REMOTE_ADDR")
    try:
        if request.user.is_authenticated:
            viewer_id = request.data.get("viewer_id")
            viewer = Viewer.objects.get(id=viewer_id)
            pk = request.data.get("video_id")
            video = Video.objects.get(id=pk)
            view = VideoView(viewer=viewer, video=video, viewer_ip=viewer_ip)
            view.save()

            try:
                history = History.objects.get(viewer=viewer)

            except:
                history = History(viewer=viewer)
                history.save()

            history.views.add(view)

            # The python approach, lie there and wait
            previous_view = 0
            previous_views = video.videoview_set.order_by("viewed_on").filter(viewer=viewer).reverse().in_bulk().values()  # type: ignore
            if len(previous_views) > 1:
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
            return Response(status=status.HTTP_200_OK)
        else:
            pk = request.data.get("video_id")
            video = Video.objects.get(id=pk)
            view = VideoView(video=video, viewer_ip=viewer_ip)
            view.save()
            video.save()

            # previous_views=[]
            previous_views = video.videoview_set.order_by("viewed_on").filter(viewer_ip=viewer_ip).reverse().in_bulk().values()  # type: ignore
            if len(previous_views) > 1:
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
            return Response(status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Viewer.DoesNotExist:
        return Response({"error": "Viewer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
