var clipboard = new Clipboard(".btn");

clipboard.on('success', function(e) {
    $('#flashes').append('<p class="info">Link copied to clipboard.</p>');
});

clipboard.on('error', function(e) {
    console.log(e);
});
