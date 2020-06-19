$('.day-wrapper').click(function() {
  var date = $(this).attr('date');

  $('#appointment-form').modal('show');
})