from django.http import HttpResponseRedirect
from django.urls import reverse

def login_required(view_func, login_url=None):
    def wrap(request, *args, **kwargs):
        if 'admin' in request.session and request.session['admin'] != None:
            return view_func(request, *args, **kwargs)
        else:
            if login_url:
                return HttpResponseRedirect(login_url)
            return HttpResponseRedirect(reverse('logout'))
    return wrap