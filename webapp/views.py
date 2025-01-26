from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CaptchaStandaloneForm
from .models import Room, Message
from .misc import get_client_ip
from . import namekeys
import re


def homepage(request, **kwargs):
    if request.POST:
        return HttpResponseRedirect(f"/{request.POST['findroom']}/")
    else:
        return render(request, 'homepage.html')

def room(request, **kwargs):
    #print(request.session.get("room_entry"))
    # various checks
    captcha_passed = False
    if request.session.get("captcha_passed", True):
        captcha_passed = True
    if captcha_passed == False:
        return HttpResponseRedirect('entry?err=captcha_failed')
    if request.session.get("room_entry") == None:
        return HttpResponseRedirect('enter')
    # now for the real stuff...
    if request.POST:                # POST #
        # limits
        if len(request.POST.get("msg")) >= 5000:
            return HttpResponseRedirect('?err=msg_over')
        # create message model
        newmsg = Message(
            author_namekey = request.session.get("room_entry"),
            author_ip = get_client_ip(request),
            message = request.POST.get("msg"),
            room = Room.objects.get(id=kwargs["room"])
        )
        newmsg.save()
        return HttpResponseRedirect('')
    else:                           # GET #
        room = Room.objects.get(id=kwargs["room"])
        messages = Message.objects.filter(room=room)
        your_name = namekeys.decouple_nk_to_name(request.session.get("room_entry"))
        your_nk_hash = namekeys.hash_nk(request.session.get("room_entry"))
        your_nk_hash_trunc = namekeys.hash_nk_trunc(request.session.get("room_entry")) # could be done in template?
        ctxt = {
            'room': room,
            'messages': messages,
            'your_name': your_name,
            'your_nk_hash': your_nk_hash,
            'your_nk_hash_trunc': your_nk_hash_trunc,
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
        # limits
        if len(request.POST['nickname']) >= 90:
            return HttpResponseRedirect('?err=nick_over')
        if len(request.POST['nickname']) <= 1:
            return HttpResponseRedirect('?err=nick_under')
        if len(request.POST['uniquekey']) >= 500:
            return HttpResponseRedirect('?err=key_over')
        if len(request.POST['unique']) <= 4:
            return HttpResponseRedirect('?err=key_under')
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
        # limits
        if len(request.POST['description']) >= 3000:
            return HttpResponseRedirect('?err=desc_over')
        if len(request.POST['password']) <= 5:
            return HttpResponseRedirect('?err=password_under')
        if len(request.POST['url']) => 50:
            return HttpResponseRedirect('?err=url_over')
        if len(request.POST['editcode']) <= 50:
            return HttpResponseRedirect('?err=editcode_under')
        # password 
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
