function register_event(event, isEvent)
{
	if(!confirm("Are you sure you want to register ? "))
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
        alert("There was an issue with your request. Please check your connection and try again !");
    else
    {
        try{
            if(msg.status != 200)
                alert(msg.errors);
            else
            {
                if(isEvent)
                    after_reg_txt = " Registered ! ";
                else
                    after_reg_txt = " Registered ! Click <a href=\"https://www.thecollegefever.com/events/synergy-ObTEcQ3mgk\">Here</a> to pay";

                alert("Registered for event ! If the event or workshop requires you to pay, remember that your seat isn't confirmed until you pay. Visit \"https://www.thecollegefever.com/events/synergy-ObTEcQ3mgk\" to pay (If applicable)");
                span = event.parentElement;
                span.innerHTML = after_reg_txt;
            }

        }
        catch(e){
            alert("There was an issue with your request. Please try again !");
        }
    }

    });
}
