
function request(after_func, form) {
	console.log(form.attr("data-purpose"))
    
    $.ajax({

		url:"/"+form.attr("data-purpose"),
		method:"POST",
		data:form.serialize(),
		timeout:20000,
		beforeSend:function(){
			console.log(" loading .. ")
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
    .done(function (msg) {
        if (msg.status == 200) {
            if (form.attr("data-purpose") === "register") {
                alert("Thank you for registering! You\'re about to be redirected to the login page.");
                window.location.href = "/login";
            } else {
                after_func(msg);
            }
        } else {
            after_func(msg);
        }
    });
		// function(msg)
		// {
		// 	error_div= $('.all-errors');
			
		// 	// if(msg=='1')
		// 	// 	window.location.reload();
		// 	// else
		// 	// {
		// 		error_div.html(msg);
		// 	// 	error_div.show();
		// 	// }
			
		// }

		// );
}

function request_event(event_num) {

}