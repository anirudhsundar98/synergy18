function register_event(event, isEvent)
{
    return;  // Registrations Closed
	if(!confirm("Are you sure you want to register? "))
		return;

    data = {'event': event.getAttribute('data-event')};

    $.ajax({

    url:"/events/register/",
    method:"POST",
    data:data,
    timeout:20000,
    beforeSend:function(){
        // $('#loading').show();
    },
    complete:function(){
        // $('#loading').hide();
    },
    error:function(err)
    {
        error_div= $('.all-errors');
        error_div.html(err);
        error_div.show();
    }

})
.done(function(msg){

    if(typeof(msg) != "object")
        alert("There was an issue with your request. Please check your connection and try again.");
    else
    {
        try{
            if(msg.status != 200)
                alert(msg.errors);
            else
            {
                // if(isEvent)
                    // after_reg_txt = " Registered";
                // else
                after_reg_txt = `Registered. Click <a href="https://allevents.in/org/synergy-nit-trichy/14792816">here</a> to pay. <br> Click <a href="/myQR" target="_blank">here</a> for your unique Synergy ID.`;

                alert("Registered successfully. Events require a general registration fee while each individual workshop requires separate payment. Workshop seats aren't confirmed until you pay. Visit \"https://allevents.in/org/synergy-nit-trichy/14792816\" to pay.");
                // alert("Registered successfully");
                span = event.parentElement;
                span.innerHTML = after_reg_txt;
            }

        }
        catch(e){
            alert("There was an issue with your request. Please try again.");
        }
    }

    });
}
