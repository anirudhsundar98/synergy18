
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
	.done(after_func);
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