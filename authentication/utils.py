from django.http import HttpResponseRedirect
def lr(view):
    def new_view(request,*args,**kwargs):
        return view(request,*args,**kwargs)
    return new_view
