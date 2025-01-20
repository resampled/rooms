from django.shortcuts import render
from .forms import CaptchaStandaloneForm

def test_txt(request, **kwargs):
    return render(request,'test.txt',content_type='text/plain')

def base_test(request, **kwargs):
    return render(request, '_base_dialog.html')

def enter_room(request, **kwargs):
    room = kwargs["room"]
    if request.POST:
        captcha = CaptchaStandaloneForm(request.POST)
        if captcha.is_valid():
            human = True
    else:
        captcha = CaptchaStandaloneForm()
        ctxt = {
            'captcha': captcha,
            'room': room,
        }
        return render(request, 'dialog/enter_room.html', context=ctxt)

def create_room(request, **kwargs):
    if request.POST:
        captcha = CaptchaStandaloneForm(request.POST)
        if captcha.is_valid():
            human = True
    else:
        captcha = CaptchaStandaloneForm()
        ctxt = {
            'captcha': captcha,
        }
        return render(request, 'dialog/create_room.html',context=ctxt)
