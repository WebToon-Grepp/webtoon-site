const $gridView = $('.grid-view');
const $listView = $('.list-view');

let titleIdType = NaN;
let titlePlatformType = NaN;

let filterType = 'all';
let platformType = 'all';
let genreType = 'all';
let sortType = 'views';
let displayType = 'grid';

$(document).ready(function() {
    $('.display-grid').click(function(e) {
        e.preventDefault();
        displayType = 'grid';
        switchToView($gridView, 'flex');
    });

    $('.display-list').click(function(e) {
        e.preventDefault();
        displayType = 'list';
        switchToView($listView, 'block');
    });

    $('.filter').click(function(e){
        e.preventDefault(); 
        $('.filter').css({ 'background-color': '', 'color': '', 'border-bottom': '' });
        $(this).css({ 'background-color': '#f5f6f7', 'color': '#1e2a3c', 'border-bottom': '3px solid #1e2a3c' });

        filterType = $(this).data('filter');
        if (filterType === 'completed') {
            genreType = 'all';
            $('#sort-genre option').hide();
            $('#sort-genre').val(genreType);
        } else {
            $('#sort-genre option').show();
        }
        switchToView(displayType === 'grid' ? $gridView : $listView, displayType === 'grid' ? 'flex' : 'block');
        loadContent();
    });

    $('.sort-option').change(function(e){
        e.preventDefault(); 
        platformType = $('#sort-platform').val();
        genreType = $('#sort-genre').val();
        sortType = $('#sort-order').val();
        switchToView(displayType === 'grid' ? $gridView : $listView, displayType === 'grid' ? 'flex' : 'block');
        loadContent();
    });

    switchToView($gridView, 'flex');
    loadContent();  
    loadGenres();  
});

function loadContent() {
    updateToDisplay(true, true, false);
    $.ajax({
        url: '/content', 
        method: 'GET',
        data: { filter: filterType, platform: platformType, genre: genreType, sort: sortType },
        success: function(response) {
            $('.grid-view').html(response.grid);
            $('.list-view').html(response.list);
        },
        error: function(error) {
            console.error('Error ajax request:', error);
        }
    });
}

function loadGenres() {
    $.ajax({
        url: '/genres', 
        method: 'GET',
        success: function(response) {
            $('#sort-genre').html(response.genres);
        },
        error: function(error) {
            console.error('Error ajax request:', error);
        }
    });
}

