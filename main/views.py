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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import django.utils.simplejson as json
@login_required
def feed(request):
    print "gereee"

    user = request.user
    user_genres = user.genretouser.all()
    feed_set = []
    for g in user_genres:
        l = Links.objects.filter(genre=g)
        for link in l:
          if link!=[]:
            feed_set.append(link)
    paginator = Paginator(feed_set, 5)
    page = request.GET.get('page')
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feeds = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feeds = paginator.page(paginator.num_pages)
    pform = PostForm()
    var = RequestContext(request,{
        'form'  : pform,
        'user'  : request.user,
        'feeds' : feeds,
        'paginator':paginator,
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
          if title not in "":
            message="success"
            user = request.user
            print user
            print content
            decision = classify_link(content)
            genre = Genre.objects.get(title=decision)
            link = Links.objects.create(title = title , content = content,user = user,genre = genre,url = url,img_src=img_src)
            links_set = []
            print decision
            links_set = Links.objects.filter(genre=genre)
            count = len(links_set)
            print count
            if count > 3:
              closest = 2
              for l in links_set:
               if l.id != link.id:
                dist = find_similar(l.content,content)
                if dist < closest:
                   closest = dist
                   new_link = l
                print new_link.title

    else:
        message = "Not called via post"
    return HttpResponse(message)
@login_required

def genrefeed(request,genre):
    g = Genre.objects.get(title=genre)
    status = "Follow"
    user = request.user
    gs = user.genretouser.all()
    if g in gs:
        status = "Following"
    links = Links.objects.filter(genre=g)
    var = RequestContext(request,{
        'feeds' : links,
        'title' :g.title,
        'status':status,
        })
    return render_to_response("main/genre.html",var)

