import { API_URL } from "../constants";

function toggleItem(id:string, toggle:boolean) {
        let element = document.getElementById(id);
        if (element) {element.style.display = (toggle) ? 'block' : 'none';}
}
    
export const handleAddToPlaylist = (event:Event, videoId:number, playlistId:number) =>{
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: (API_URL+"add_video_to_playlist"),
        data: {
            video_id: videoId,
            playlist_id: playlistId
        },
        success: function() {
            // toggleItem(addButtonId, false);
            // toggleItem(successId, true);
        },
    });
}

export const handleRemoveFromPlaylist = (event:Event, videoId:number, playlistId:number) => {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: (API_URL+"remove_video_from_playlist"),
        data: {
            video_id: videoId,
            playlist_id: playlistId
        },
        success: function() {
            // toggleItem(addButtonId, false);
            // toggleItem(successId, true);
        },
    });
}

export const handleAddToWatchlater = (event:Event, videoId:string, addButtonId:string, successId:string) =>{
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: (API_URL+"add_video_to_watchlater"),
        data: {
            video_id: videoId,
        },
        success: function() {
            toggleItem(addButtonId, false);
            toggleItem(successId, true);
        },
    });
}

export const handleRemoveFromWatchlater = (event:Event, videoId:string, addButtonId:string, successId:string) =>{
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: (API_URL+"remove_video_from_watchlater"),
        data: {
            video_id: videoId,
        },
        success: function() {
            toggleItem(addButtonId, false);
            toggleItem(successId, true);
        },
    });
}