var clipboard = new Clipboard(".btn");

clipboard.on('success', function(e) {
    $(e.trigger).attr('title', 'Link Copied').tooltip('fixTitle').tooltip('show');
});

clipboard.on('error', function(e) {
    console.log(e);
});
