$(function() {
    var since = 0;
    setInterval(function() {
      var tzoffset = (new Date()).getTimezoneOffset() * 60000;
      var currTime = new Date(Date.now() - tzoffset).getTime()/1000;
      console.log('Ajax request submitted');
      $.ajax(
        {
          url:'/appointments/notifications',
          type:'POST',
          data:{
            'currTime':currTime
          }
        }
      )
      .done(
        function(data) {
          console.log(data.messages);
          for (const message in data.messages) {
            console.log(data.messages[message]);
          }
        }
      )
  }, 10000);
});