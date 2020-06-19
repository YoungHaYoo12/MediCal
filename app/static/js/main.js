$('.day-wrapper').click(function() {
  var date = $(this).attr('date');

  $('#appointment-form').modal('show');

  $.ajax(
    {
      url:'/calendars/create/event',
      type: 'POST',
      data: {
        date:date
      }

    }
  )
  .done(
    function(data) {
      if (data.result == 'success') {
        console.log('SUCCESS')
      }
    }
  )
})