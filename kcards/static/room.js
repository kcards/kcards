setInterval(function() {
    $.ajax({

      type: "GET",
      url: "/api/rooms/" + code + "/timestamp",
      datatype: "JSON",

      success: function(data) {
          if (data["timestamp"] != timestamp) {
            location.reload();
          };
      }

    });
}, 1000);
