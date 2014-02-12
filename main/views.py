# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response , get_object_or_404,render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.models import *
from main.models import *
from goose import Goose
from main.forms import *
from main.utils import *
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import django.utils.simplejson as json
@login_required
def feed(request):
    print "gereee"
    user = request.user
    user_genres = user.genretouser.all()
    post_displayed = []
    feeds = Links.objects.all()
    pform = PostForm()
    var = RequestContext(request,{
        'form'  : pform,
        'user'  : request.user,
        'feeds' : feeds,
      })
    return render_to_response("main/dashboard.html",var)

def profile(request,username):
    visitor = request.user
    user = get_object_or_404(User,username = username)
    links = Links.objects.filter(user=user).order_by('posted_time')
    var = RequestContext(request,{
        'user':user,
        'visitor':visitor,
        'links' : links,
        })
    return render_to_response('main/profile.html',var)

@login_required
@csrf_exempt
def categorize_links(request):
    message = ""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
          url = form.cleaned_data['content'] 
          print url
          title,content,img_src = extract_content(url)
	  print title
          if title not in "":
           message="success"
           user = request.user
           print user	
           genre = Genre.objects.get(title='Food')
           link = Links.objects.create(title = title , content = content,user = user,genre = genre,url = url,img_src=img_src)
    else:
        message = "Not called via post"
    return HttpResponse(message)
