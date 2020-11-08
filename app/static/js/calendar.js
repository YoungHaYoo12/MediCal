document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left:"dayGridMonth,timeGridWeek,timeGridDay listMonth,listWeek,listDay",
      center:'title',
      right:'custom1 prevYear,prev,next,nextYear'
    },
    buttonText: {
      listMonth:'list month',
      listWeek:'list week',
      listDay:'list day'
    },
    customButtons: {
      custom1: {
        text:'Create',
        click: function(){
          $('#appointment-form').modal('show');
          // set date_start and date_end to current time in user's timezone
          var tzoffset = (new Date()).getTimezoneOffset() * 60000;
          var currTime = new Date(Date.now() - tzoffset).toISOString().slice(0,-8);
          $('#date_start').val(currTime);
          $('#date_end').val(currTime);
        }
      }
    },
    timeZone:'local',
    editable:true,
    navLinks:true,
    selectable:true,
    select: function(selectionInfo){
      var date_start = selectionInfo.startStr;
      var date_end = selectionInfo.endStr;
      if (date_start.indexOf('T') == -1) {
        date_start = date_start + 'T12:00';
      } else if (date_start.indexOf('+') != -1) {
        date_start = date_start.split('+')[0];
        date_start = date_start.slice(0,-3);
      }
      if (date_end.indexOf('T') == -1) {
        date_end = date_end + 'T12:00';
      } else if (date_end.indexOf('+') != -1) {
        date_end = date_end.split('+')[0];
        date_end = date_end.slice(0,-3);
      }
      $('#appointment-form').modal('show');
      $('#date_start').val(date_start)
      $('#date_end').val(date_end)
    },
    selectMirror:true,
    eventDrop:function(info) {
      alert(info.event.title + " was dropped on " + info.event.start.toISOString());
      if (!confirm("Are you sure about this change?")) {
        info.revert();
      }
      else {
        $.ajax(
          {
            url:'/appointments/move-appointment',
            type:'POST',
            data:{
              'appointment_id':info.event.id,
              'start':info.event.startStr,
              'end':info.event.endStr
            }
          }
        )
        .done(
          function(data) {
            if(data.result=='success'){
              console.log('success!')
              console.log(info.event.backgroundColor)
            }
          }
        )
      }
    },
    eventResize: function(info) {
      alert(info.event.title + " end is now " + info.event.end.toISOString());
      if (!confirm("Is this okay?")) {
        info.revert();
      }
      else {
        $.ajax(
          {
            url:'/appointments/move-appointment',
            type:'POST',
            data:{
              'appointment_id':info.event.id,
              'start':info.event.startStr,
              'end':info.event.endStr
            }
          }
        )
        .done(
          function(data) {
            if(data.result=='success'){
              console.log('success!')
            }
          }
        )
      } 
    },
    events: function(info,successCallback,failureCallback) {
      $.ajax(
      {
        url:'/appointments/data',
        type:'POST',
        data: {},
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

              // filtering
              var display = 'none';
              var user_id = $('.user').val();
              var patient_id = $('.patient').val();
              var treatment_id = $('.treatment').val();
              var status = $('.status').val();

              if ((e.user_id == user_id || user_id =='all') && 
                  (e.patient_id == patient_id || patient_id =='all') &&
                  (e.treatment_id == treatment_id || treatment_id =='all') &&
                  (e.status == status || status == 'all')) {
                    display = "auto";
                  }

              events.push({
                id:e.id,
                title:e.title,
                start:e.start,
                end:e.end,
                allDay:allDay,
                backgroundColor:e.color,
                display:display
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
            if (data.appointment_status == 'complete') {
              $('#status-btn').html(
                '<button class="btn btn-secondary"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-calendar-check-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM0 5h16v9a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V5zm10.854 3.854a.5.5 0 0 0-.708-.708L7.5 10.793 6.354 9.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/></svg></button>'
              );
            } else{
            $('#status-btn').html(
              '<button class="btn btn-secondary"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-calendar-minus-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM0 5h16v9a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V5zm6 5a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1H6z"/></svg></button>'
            );
            }

            // links to patient, user, toggle_is_completed
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

            // links to buttons
            var link = "/appointments/edit/" + data.appointment_id;
            $('#appointment-edit-btn').attr('href',link);

            var link = "/appointments/delete/" + data.appointment_id;
            $('#appointment-delete-btn').attr('href',link);

            var link = "/appointments/toggle_status/" + data.appointment_id;
            $('#status-btn').attr('href',link);

            $('#appointment-info-modal').modal('show');

          }
        }
      )  
    }
  });
  calendar.render();
});
