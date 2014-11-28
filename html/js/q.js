$(document).ready(function(){
  
  $("#searchb").click(function(){
  //   $( "#results" ).load( 
  //     "results.json", 
  //     function(){
  //     });
  // });

    email = $("#email").val();
    eventid = $("#eventid").val();

    $.ajax({
      type: "GET",
      url: "http://localhost:8081/getmatches",
      data: { email: email, event_id: eventid },
      dataType: "json",
    }).done(function(msg, textStatus, request) {
      console.log(msg)
      if(msg.length > 0) {
        var res = "";
        for(var i=0; i<msg.length; i++) {
          res = res + msg[i]['name'] + ", ";
        }

        $('#results').html('I have matched you with ' + res);
      }
    }).fail(function(jqXHR, textStatus) {
      console.log(jqXHR);
      console.log(textStatus);
      $('#results').html('Apologies, I have been unable to match you with anyone');
    });

  });

})
