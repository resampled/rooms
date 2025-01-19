from django import forms
from captcha.fields import CaptchaField

class CaptchaStandaloneForm(forms.Form):
    captcha = CaptchaField()
