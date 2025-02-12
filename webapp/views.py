from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CaptchaStandaloneForm
from .models import Room, Message
from .misc import get_client_ip, elist_append, elist_find
from . import namekeys
import re


def homepage(request, **kwargs):
    if request.POST:
        return HttpResponseRedirect(f"/{request.POST['findroom']}/")
    else:
        return render(request, 'homepage.html')

def room(request, **kwargs):
    #print(request.session.get("room_entry"))
    room = Room.objects.get(id=kwargs["room"])
    # various checks
    if request.session.get("room_entry") == None:
        return HttpResponseRedirect('enter')
    if "room_entry" in request.session and elist_find(room.banned_nk,request.session["room_entry"]) == True: # if nk kicked from room
        return HttpResponseRedirect('kicked')
    # captccha
    captcha_passed = False
    if request.session.get("captcha_passed", True):
        captcha_passed = True
    if captcha_passed == False:
        return HttpResponseRedirect('entry?err=captcha_failed')
    if room.passworded == True:
        if "room_pwd" not in request.session or request.session["room_pwd"] != room.password:
            return HttpResponseRedirect('pwd')
    # now for the real stuff...
    if request.POST:                # POST #
        # limits
        if len(request.POST.get("msg")) >= 2000:
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
        err = None
        if 'err' in request.GET:
            err = request.GET.get('err')
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
            'err': err,
        }
        return render(request, 'room.html', context=ctxt)

def enter_room(request, **kwargs):
    room = Room.objects.get(id=kwargs["room"])
    if "room_entry" in request.session and elist_find(room.banned_nk,request.session["room_entry"]) == True: # if nk kicked from room
        return HttpResponseRedirect('kicked')
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
        if len(request.POST['uniquekey']) <= 4:
            return HttpResponseRedirect('?err=key_under')
        cookie_content = namekeys.generate_nk_combo(request.POST['nickname'],request.POST['uniquekey'])
        if cookie_content == '0':
            return HttpResponseRedirect('?err=nick_invchar')
        response = HttpResponseRedirect('.') # to room
        request.session["room_entry"] = cookie_content
        # response.set_cookie(key='room_entry_do_not_share',value=cookie_content,max_age=3000000,httponly=True,samesite="Lax")
        # maybe store in sessionstorage instead?
        return response
    else: # GET
        err = None
        if 'err' in request.GET:
            err = request.GET.get('err')
        captcha = CaptchaStandaloneForm()
        ctxt = {
            'captcha': captcha,
            'room': room,
            'err': err,
        }
        return render(request, 'dialog/enter_room.html', context=ctxt)

def edit_room(request, **kwargs):
    room = Room.objects.get(id=kwargs["room"])
    messages = Message.objects.filter(room=room).order_by('id')
    if request.session["editcode"] != room.edit_code:
        return HttpResponseRedirect('editcode?err=editcode_fail')
    if request.POST:
        if 'settings-form' in request.POST:
            # todo: handle settings change <---------
            return HttpResponseRedirect('?rsp=0')
        if 'msgaction-form' in request.POST:
            if Message.objects.get(id=request.POST['msgaction-form']).room != room:
                return HttpResponseRedirect('?err=wtf') # if message isn't in this room (form hacking)
            target = Message.objects.get(id=request.POST['msgaction-form'])
            if 'delete' in request.POST:
                target.delete()
                return HttpResponseRedirect('?rsp=msgaction-delete')
            if 'kick' in request.POST:
                room.banned_nk = elist_append(room.banned_nk,target.author_namekey) # append nk to banned_nk elist
                room.save()
                return HttpResponseRedirect('?rsp=msgaction-kick')
            if 'delall' in request.POST:
                targets = Message.objects.filter(author_namekey=target.author_namekey)
                for target_item in targets:
                    target_item.delete()
                return HttpResponseRedirect('?rsp=msgaction-delall')
    else:
        ctxt = {
            'room': room,
            'messages': messages,
        }
        return render(request, 'edit_room.html', context=ctxt)

def edit_room_editcode(request, **kwargs):
    if request.POST:
        if len(request.POST["editcode"]) >= 500:
            return HttpResponseRedirect('?err=editcode_over')
        request.session["editcode"] = request.POST["editcode"]
        return HttpResponseRedirect('edit')
    else:
        return render(request, 'dialog/edit_room_editcode.html')

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
        if len(request.POST['password']) <= 5 and len(request.POST['password']) != 0:
            return HttpResponseRedirect('?err=password_under')
        if len(request.POST['password']) >= 500:
            return HttpResponseRedirect('?err=password_over')
        if len(request.POST['url']) >= 50:
            return HttpResponseRedirect('?err=url_over')
        if len(request.POST['editcode']) <= 5:
            return HttpResponseRedirect('?err=editcode_under')
        if len(request.POST['editcode']) >= 500:
            return HttpResponseRedirect('?err=editcode_over')
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
            banned_nk='',
        )
        gen_room.save()
        return HttpResponseRedirect(f"/{request.POST['url']}/")
    else: # GET
        err = None
        if 'err' in request.GET:
            err = request.GET.get('err')
        captcha = CaptchaStandaloneForm()
        ctxt = {
            'captcha': captcha,
            'err': err,
        }
        return render(request, 'dialog/create_room.html',context=ctxt)

def kicked_room(request, **kwargs):
    room = Room.objects.get(id=kwargs["room"])
    # if no namekey
    if "room_entry" not in request.session:
        return HttpResponseRedirect('./enter')
    # if namekey not kicked
    if "room_entry" in request.session and elist_find(room.banned_nk,request.session["room_entry"]) == False:
        return HttpResponseRedirect('.')
    ctxt = {
        'room': room,
    }
    return render(request, 'dialog/kicked.html', context=ctxt)

def passworded_room(request, **kwargs): # todo: perhaps merge this with room_entry?
    room = Room.objects.get(id=kwargs["room"])
    # if not passworded
    if room.passworded == False:
        if "room_entry" in request.session:
            return HttpResponseRedirect('.')
        else:
            return HttpResponseRedirect('./enter')
    if request.POST:
        if len(request.POST['pwd']) >= 500:
            return HttpResponseRedirect('?err=password_over')
        request.session['room_pwd'] = request.POST['pwd']
        return HttpResponseRedirect('.')
    else:
        err = None
        if 'err' in request.GET:
            err = request.GET.get('err')
        ctxt = {
            'room': room,
            'err': err,
        }
        return render(request, 'dialog/passworded.html', context=ctxt)
