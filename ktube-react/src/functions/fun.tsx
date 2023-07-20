function toggleItem(id:string, toggle:boolean) {
        let element = document.getElementById(id);
        if (element) {element.style.display = (toggle) ? 'block' : 'none';}
}
    
export const handleAddToPlaylist = (event:Event, videoId:string, playlistId:string, addButtonId:string, successId:string) =>{
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: "{% url 'add_video_to_playlist' %}",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            video_id: videoId,
            playlist_id: playlistId
        },
        success: function() {
            toggleItem(addButtonId, false);
            toggleItem(successId, true);
        },
    });
}

export const handleRemoveFromPlaylist = (event:Event, videoId:string, playlistId:string, addButtonId:string, successId:string) => {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: "{% url 'remove_video_from_playlist' %}",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            video_id: videoId,
            playlist_id: playlistId
        },
        success: function() {
            toggleItem(addButtonId, false);
            toggleItem(successId, true);
        },
    });
}

export const handleAddToWatchlater = (event:Event, videoId:string, addButtonId:string, successId:string) =>{
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: "{% url 'add_video_to_watchlater' %}",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}",
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
        url: "{% url 'remove_video_from_watchlater' %}",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            video_id: videoId,
        },
        success: function() {
            toggleItem(addButtonId, false);
            toggleItem(successId, true);
        },
    });
}