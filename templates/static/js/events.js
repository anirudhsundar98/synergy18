function register_event(event)
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
                alert("Registered for event !");
                span = event.parentElement;
                span.innerHTML = " Registered ! "
            }

        }
        catch(e){
            alert("There was an issue with your request. Please try again !");
        }
    }

    });
}
