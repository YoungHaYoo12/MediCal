$('.day-wrapper').click(function() {
  var date = $(this).attr('date');

  $('#appointment-form').modal('show');
})

// when appointment is clicked
$('.notification').click(function() {
  var appointment_id = $(this).attr('appointment_id');

  $.ajax(
    {
      url:'/calendars/appointment',
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

       $('#appointment-info-modal').modal('show');

     }
   }
 )  
})