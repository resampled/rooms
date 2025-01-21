from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CaptchaStandaloneForm
from .models import Room, Message
from . import namekeys
import re


def homepage(request, **kwargs):
    if request.POST:
        return HttpResponseRedirect(f"/{request.POST['findroom']}/")
    else:
        return render(request, 'homepage.html')

def room(request, **kwargs):
    print(request.session.get("room_entry"))
    captcha_passed = False
    if request.session.get("captcha_passed", True):
        captcha_passed = True
    if captcha_passed == False:
        return HttpResponseRedirect('entry?err=captcha_failed')
    if request.session.get("room_entry") == None:
        return HttpResponseRedirect('entry')
    # interpret cookie here
    if request.POST:                # POST #
        return HttpResponse("post")
    else:                           # GET #
        room = Room.objects.get(id=kwargs["room"])
        messages = Message.objects.filter(room=room)
        ctxt = {
            'room': room,
            'messages': messages,
        }
        return render(request, 'room.html', context=ctxt)

def enter_room(request, **kwargs):
    room = Room.objects.get(id=kwargs["room"])
    if request.POST:
        captcha = CaptchaStandaloneForm(request.POST)
        if not captcha.is_valid(): # check captcha
            return HttpResponseRedirect('?err=captcha_failed')
        else:
            request.session["captcha_passed"] = True
        # todo: create cookie and redirect to room
        cookie_content = namekeys.generate_nk_combo(request.POST['nickname'],request.POST['uniquekey'])
        if cookie_content == '0':
            return HttpResponseRedirect('?err=nick_invchar')
        response = HttpResponseRedirect('.') # to room
        request.session["room_entry"] = cookie_content
        # response.set_cookie(key='room_entry_do_not_share',value=cookie_content,max_age=3000000,httponly=True,samesite="Lax")
        # maybe store in sessionstorage instead?
        return response
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
