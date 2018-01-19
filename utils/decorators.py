#Imports
from django.http import HttpResponse, HttpResponseRedirect
from utils import general
#Decorators / Context_Manager_Helpers
def check_errors(function):
    def block(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:

            print("there was an exception : ", e.args, " ", e)
            # raise e
            return HttpResponse(e)
    return block

def jsonResponse_wrapper(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if not response.status:
            response.status = 400

    return wrapper

def check_logged_in(redirect_path, do_while_loggedin=True):
    def wrapper_0(function):
        def wrapper_1(request):
            if 'cur_token' in request.session:
                cur_user = general.auth_token_lookup(request.session["cur_token"])
                if cur_user is not None:
                    if do_while_loggedin:
                        print(" we were here ")
                        return function(request)
                    return HttpResponseRedirect(redirect_path)
                else:
                    if not do_while_loggedin:
                        request.session.pop("cur_token")
                        return function(request)
                    return HttpResponseRedirect(redirect_path)
            else:
                if not do_while_loggedin:
                    return function(request)
            return HttpResponseRedirect(redirect_path)
        return wrapper_1
    return wrapper_0