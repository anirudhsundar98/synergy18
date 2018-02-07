captcha = Vue.component('captcha', {
	props:["purpose"],
  	template: '<div v-if="purpose === \'register\'" class="g-recaptcha field half" data-sitekey="6LcmLz8UAAAAAKXZA2gw3qIPRmNGRZdPf_TDm121"></div>'
});

submit = Vue.component('submit',{
	template: `<ul class="actions text-center">
        <li style="float:left;"><input class="special" type="submit" value="Submit"/></li>
    </ul>`
});

after_reg = Vue.component('afterReg', {

	template: `<div class="after_reg" style="display:none;">
		Thank you for registering ! Click <a href="/login">Here</a> to login 
	</div>
	`
});

new Vue({
	
	el:"#wrapper",
});