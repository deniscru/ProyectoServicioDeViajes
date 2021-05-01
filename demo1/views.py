from django.shortcuts import render

def principal(request):
    return render(request, 'demo1/principal.html', {})
