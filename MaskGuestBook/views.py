from django.shortcuts import render, redirect
from .forms import GuestBookForm

# Create your views here.
def GuestBook(request):
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
        return render(
            request,
            'MaskGuestBook/GuestBook.html',
            {'form': form}
        )

def index(request):

    return render(
        request,
        'MaskGuestBook/index.html',
        {
        }
    )
