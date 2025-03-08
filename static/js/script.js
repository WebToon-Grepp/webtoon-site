function updateToDisplay() {
    fadeChange($('.view-contents'));
}

function switchToView(viewToShow, displayStyle) {
    const views = [$gridView, $listView];
    views.forEach(view => {
        if (view !== viewToShow) fadeOut(view);
    });
    fadeIn(viewToShow, displayStyle);
}

function fadeChange(view) {
    $(view).animate({ opacity: 0 }, 100, function() {
        $(view).animate({ opacity: 1 }, 500);
    });
}

function fadeIn(view, display) {
    $(view).css("display", display); 
    $(view).css("opacity", 0); 
    $(view).animate({ opacity: 1 }, 10); 
}

function fadeOut(view) {
    view.hide()
    $(view).animate({ opacity: 0 }, 300, function() {
        $(view).css("display", "none"); 
    });
}
