# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.views import *
from django.shortcuts import render_to_response
from videogallery.forms import *

def main_page(request):
    return render_to_response(
        'main_page.html', RequestContext(request)
)

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(u'Requested user not found.')
    videos = user.video_set.all()
    template = get_template('user_page.html')
    variables = RequestContext(request, {
            'username': username,
            'videos': videos
    })
    output = template.render(variables)
    return render_to_response('user_page.html', variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email']
                )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)

def video_upload_page(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            # Link, or videofile. Whatever, I don't even.
            link, dummy = VideoFile.objects.get_or_create(
                videofile = form.cleaned_data['video']
            )
            # Video
            video, created = Video.objects.get_or_create(
                user=request.user
                videofile = link
            )
            video.title = form.cleaned_data['title']
            if not created:
                bookmark.
                
