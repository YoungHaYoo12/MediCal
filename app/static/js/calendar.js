document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left:'dayGridMonth,timeGridWeek,timeGridDay',
      center:'title',
      right:'custom1 prevYear,prev,next,nextYear'
    },
    customButtons: {
      custom1: {
        text:'Create',
        click: function(){
          $('#appointment-form').modal('show');
        }
      }
    },
    editable:true,
    eventDrop:function(info) {
      alert(info.event.title + " was dropped on " + info.event.start.toISOString());
      if (!confirm("Are you sure about this change?")) {
        info.revert();
      }
      else {
        $.ajax(
          {
            url:'/appointments/edit-appointment',
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
            url:'/appointments/edit-appointment',
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

              if ((e.user_id == user_id || user_id =='all') && 
                  (e.patient_id == patient_id || patient_id =='all') &&
                  (e.treatment_id == treatment_id || treatment_id =='all')) {
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
    }
  });
  calendar.render();
});