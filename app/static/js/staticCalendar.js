document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left:"dayGridMonth listMonth",
      center:'title',
      right:'prevYear,prev,next,nextYear'
    },
    buttonText: {
      listMonth:'list',
      dayGridMonth:'calendar',
    },
    events: function(info,successCallback,failureCallback) {
      var model = $('#calendar-tag').attr('model');
      var model_id = $('#calendar-tag').attr('model_id');

      $.ajax(
      {
        url:'/appointments/data',
        type:'POST',
        data: {
          'model':model,
          'model_id':model_id
        },
      })
      .done(
        function(data) {

          if (data.result == 'success') {
            var events = [];
            $.each(data.appointments_data,function(idx,e){
              var allDay;
              if (e.allDay == "true") {
                allDay = true;
              } else {
                allDay = false;
              }

              events.push({
                id:e.id,
                title:e.title,
                start:e.start,
                end:e.end,
                allDay:allDay,
                backgroundColor:e.color,
              })
            })
            successCallback(events)
          }
        }
      )
    },
    eventClick: function(info) {
      $.ajax(
      {
        url:'/appointments/appointment',
        type:'POST',
        data: {
          'appointment_id':info.event.id
        },
      })
      .done(
        function(data) {
          if (data.result == 'success') {
            console.log('SUCCESS')
            // fill in appointment information text
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

            // links to patient, user
            var link = "/patients/patient/" + data.patient_id;
            $('.appointment-info-modal-patient-link').attr('href',link);

            var link = "/user/" + data.user_username;
            $('.appointment-info-modal-user-link').attr('href',link);

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
    }
  });
  calendar.render();
});