from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404,redirect,render
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import logout , login,authenticate
from django.forms import *
from authentication.forms import *
from authentication.models import *
def landing(request):
   return render_to_response('registration/landing.html')
def home(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['firstname'],
                    last_name = form.cleaned_data['lastname'],
                    )

            authuser = authenticate(username=form.cleaned_data['username'],password = form.cleaned_data['password'])
            if authuser is not None:
                login(request,authuser)
            return HttpResponseRedirect('/accounts/step2/')

    else:
      form = SignUpForm()
    var = RequestContext(request,{
        'form': form,
        })
    return render_to_response('registration/signup.html',var)
def step2(request):
    genre_list = Genre.objects.all()
    var = RequestContext(request,{
        'username' : request.user,
        'genre_list':genre_list,
        })
    return render_to_response('registration/signup2.html',var);
def follow_topic(request,topic):
    user = request.user
    topic = Genre.objects.get(title = topic)
    if topic in user.genretouser.all():
        user.genretouser.remove(topic)
    else:
        user.genretouser.add(topic)
    return HttpResponse("success")



