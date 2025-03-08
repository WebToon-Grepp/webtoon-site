let sortType = 'id';

$(document).ready(function() {
    $('.sort-order').change(function(e){
        e.preventDefault(); 
        sortType = $('.sort-order').val();
        loadEpisode();
    });
    
    loadTitle();
    loadEpisode();
});

function loadEpisode() {
    updateToDisplay();
    $.ajax({
        url: '/episode/content', 
        method: 'GET',
        data: { id: titleIdType, platform: titlePlatformType, sort: sortType },
        success: function(response) {
            $('.episode-view').html(response.episode);
        },
        error: function(error) {
            console.error('Error ajax request:', error);
        }
    });
}

function loadTitle() {
    updateToDisplay();
    $.ajax({
        url: '/title/content', 
        method: 'GET',
        data: { id: titleIdType, platform: titlePlatformType },
        success: function(response) {
            $('.title-view').html(response.title);
        },
        error: function(error) {
            console.error('Error ajax request:', error);
        }
    });
}