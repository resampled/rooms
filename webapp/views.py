from django.shortcuts import render
from .forms import CaptchaStandaloneForm
from .models import Room, Message
from django.http import HttpResponseRedirect
import re

def homepage(request, **kwargs):
    if request.POST:
        return HttpResponseRedirect(f"/{request.POST['findroom']}/")
    else:
        return render(request, 'homepage.html')

def room(request, **kwargs):
    return HttpResponseRedirect('enter')

def enter_room(request, **kwargs):
    room = Room.objects.get(id=kwargs["room"])
    if request.POST:
        captcha = CaptchaStandaloneForm(request.POST)
        if not captcha.is_valid(): # check captcha
            return HttpResponseRedirect('?err=captcha_failed')
        # todo: create cookie and redirect to room
    else: # GET
        captcha = CaptchaStandaloneForm()
        ctxt = {
            'captcha': captcha,
            'room': room,
        }
        return render(request, 'dialog/enter_room.html', context=ctxt)

def create_room(request, **kwargs):
    if request.POST:
        captcha = CaptchaStandaloneForm(request.POST)
        if not captcha.is_valid(): # check captcha
            return HttpResponseRedirect('?err=captcha_failed')
        if not re.match(r'^[a-z0-9_-]*$',request.POST['url']):
            # check if url is valid slug
            return HttpResponseRedirect('?err=url_notslug')
        if Room.objects.filter(id=request.POST['url']).first() != None:
            # check if room already exists
            return HttpResponseRedirect('?err=url_exists')
        passworded = False
        if 'passworded' in request.POST:
            passworded = True
        gen_room = Room(
            id=request.POST['url'],
            edit_code=request.POST['editcode'],
            description=request.POST['description'],
            public_list=False,
            passworded=passworded,
            password=request.POST['password'],
        )
        gen_room.save()
        return HttpResponseRedirect(f"/{request.POST['url']}/")
    else: # GET
        captcha = CaptchaStandaloneForm()
        ctxt = {
            'captcha': captcha,
        }
        return render(request, 'dialog/create_room.html',context=ctxt)
