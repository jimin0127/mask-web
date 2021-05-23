from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import GuestBookForm
from .models import GuestBook

# Create your views here.
def postGuestBook(request):
    if request.method == 'POST':
        form = GuestBookForm(request.POST)
        if form.is_valid():
            form.save()
            # return render(
            #     request,
            #     'MaskGuestBook/index.html',
            #     {'form': form}
            # )
            return redirect('index')

    else:
        form = GuestBookForm()
        # return render(
        #     request,
        #     'MaskGuestBook/GuestBook.html',
        #     {'form': form}
        # )
        return render(
            request,
            'MaskGuestBook/GuestBook.html',
            {'form': form}
        )

def index(request):
    guests = {'guests':GuestBook.objects.all()}
    return render(request, 'MaskGuestBook/list.html', guests)
    # return render(
    #     request,
    #     'MaskGuestBook/index.html',
    #     {}
    # )
    # return HttpResponse(str)

def keyboard(request):
    return JsonResponse(
        {
            'type': 'buttons',
            'buttons': ['Mask란', '개발자 소개']
        }
    )


