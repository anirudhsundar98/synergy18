
	function after_req(msg) {
		if(typeof(msg) != "object")
			$(".all-errors").html("There was an issue with your request. Please try again !");
		else
		{
				if(msg.status != 200)
				{
					$(".all-errors").html(msg.errors);
					alert('Please resolve the errors and try again !');
				}
				else if(msg.hasOwnProperty('inline'))
				{
				    if(msg.inline == true)
				        alert("Done updating !");
				}
				else
				{
          // window.location.href = "http://synergy.nitt.edu";
					window.location.href = "/";

				}
//			}
//			catch(e){
//
//				$(".all-errors").html("There was an issue with your request. Please try again !");
//			}
		}

	}

	function request_form(e){


		e.preventDefault();

		form = $(".main-form");

		request(after_req, form);
	}

	$(document).ready(function(){
		$(".main-form").submit(request_form);
	});
