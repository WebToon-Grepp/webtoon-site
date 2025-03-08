const $gridView = $('.grid-view');
const $listView = $('.list-view');

let titleIdType = NaN;
let titlePlatformType = NaN;

let filterType = 'all';
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
        switchToView(displayType === 'grid' ? $gridView : $listView, displayType === 'grid' ? 'flex' : 'block');
        loadContent();
    });

    $('.sort-order').change(function(e){
        e.preventDefault(); 
        sortType = $('.sort-order').val();
        switchToView(displayType === 'grid' ? $gridView : $listView, displayType === 'grid' ? 'flex' : 'block');
        loadContent();
    });

    switchToView($gridView, 'flex');
    loadContent();  
});

function loadContent() {
    updateToDisplay(true, true, false);
    $.ajax({
        url: '/content', 
        method: 'GET',
        data: { filter: filterType, sort: sortType },
        success: function(response) {
            $('.grid-view').html(response.grid);
            $('.list-view').html(response.list);
        },
        error: function(error) {
            console.error('Error ajax request:', error);
        }
    });
}

