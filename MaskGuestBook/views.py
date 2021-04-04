from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(
        request,
        'MaskGuestBook/index.html',
        {}
    )

def keyboard(request):
    return JsonResponse(
        {
            'type': 'buttons',
            'buttons': ['Mask란', '개발자 소개']
        }
    )