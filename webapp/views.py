from django.shortcuts import render

def test_txt(request, **kwargs):
    return render(request,'test.txt',content_type='text/plain')

def base_test(request, **kwargs):
    return render(request, '_base_dialog.html')
