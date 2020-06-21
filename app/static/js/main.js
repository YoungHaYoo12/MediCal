// when appointment is clicked
$('.notification').click(function() {
  var appointment_id = $(this).attr('appointment_id');

  $.ajax(
    {
      url:'/appointments/appointment',
      type: 'POST',
      data: {
        appointment_id:appointment_id
      }
    }
  )
 .done(
   function(data) {
     if (data.result == 'success') {
       console.log('SUCCESS')
       $('#appointment-info-modal-title').text(data.appointment_title);
       $('#appointment-info-modal-description').html(
         '<span class="bold">Description: </span>' + 
         data.appointment_description
         );
       $('#appointment-info-modal-date-start').html(
         '<span class="bold">Start Time: </span>' + 
         data.appointment_date_start
         );         
       $('#appointment-info-modal-date-end').html(
         '<span class="bold">End Time: </span>' + 
         data.appointment_date_end
         );      
       $('#appointment-info-modal-treatment').html(
         '<span class="bold">Treatment: </span>' + 
         data.appointment_treatment_name
         );     
       $('#appointment-info-modal-patient').html(
         '<span class="bold">Patient: </span>' + 
         data.appointment_patient_name
         );  
       $('#appointment-info-modal-user').html(
         '<span class="bold">Doctor: </span>' + 
         data.appointment_user_username
         );   
      
       // only show buttons if current user owns appointment
       if (!data.user_is_appointment_owner) {
         $('.modal-footer').hide()
       } else{
         $('.modal-footer').show()
       }

       var link = "/appointments/edit/" + data.appointment_id;
       $('#appointment-edit-btn').attr('href',link);

       var link = "/appointments/delete/" + data.appointment_id;
       $('#appointment-delete-btn').attr('href',link);

       $('#appointment-info-modal').modal('show');

     }
   }
 )  
})

// ************************************************************************************//

var max_appointments_length = 3;
// function to hide all notifications greater than max_appointments_length (used when page is first loaded)
var showLess = function() {
  var appointments = $(this).children('.notification')
  var length = appointments.length;

  // hide notifications greater than 5
  for (var i = max_appointments_length;  i < length; i++) {
    $(appointments[i]).hide()
  }

  // display '#showMore' if greater than 5 appointments
  if (length > max_appointments_length) {
    $(this).find('.showMore').show()
  }
}
$.each($('.appointments-wrapper'),showLess)

// function to show all appointments in a .appointments-wrapper (used with .showMore button)
var expand = function() {
  var appointmentsWrapper = $(this).parent('.appointments-wrapper')
  var appointments = $(appointmentsWrapper).children('.notification')
  for (var i = 0; i < appointments.length; i++) {
    $(appointments[i]).show()
  }

  // switch showMore and showLess buttons
  $(this).hide()
  $(this).siblings('.showLess').show()
}

// function to collapse appointments in a .appointments-wrapper (used with .showLess button)
var collapse = function() {
  var appointmentsWrapper = $(this).parent('.appointments-wrapper')
  var appointments = $(appointmentsWrapper).children('.notification')
  for (var i = max_appointments_length; i < appointments.length; i++) {
    $(appointments[i]).hide()
  }

  // switch showMore and showLess buttons
  $(this).hide()
  $(this).siblings('.showMore').show()
}

// set buttons to respective methods
$('.showMore').each(
  function() {
    $(this).on("click",expand)
  }
)

$('.showLess').each(
  function() {
    $(this).on("click",collapse)
  }
)