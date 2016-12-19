function checkForUpdates() {

    console.log("Waiting for room updates...")
    $.ajax({

        type: "GET",
        url: "/api/rooms/" + code + "/timestamp?current=" + timestamp,
        datatype: "JSON",

        complete: function(data) {
            if (data["timestamp"] == timestamp) {
                console.log("No room changes")
                checkForUpdates();
            } else {
                console.log("Room changes detected")
                location.reload();
            };
        }

    });
}

checkForUpdates();
