from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

from .forms import GuestBookForm
from .models import GuestBookModel
from .playSound import playsound

from .mask_function.VideoCamera import VideoCamera
from .mask_function.Position import position
import threading
from .mask_function.camera import camera


playsound = playsound()
cam = VideoCamera()


# Create your views here.
def goGuestBook(request):
    form = GuestBookForm()
    return render(
        request,
        'MaskGuestBook/GuestBook.html',
        {'form' : form}
    )

def gen(camera):
    while True:
        frame = cam.get_frame()

        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def stream2(request):
    try:
        return StreamingHttpResponse(gen(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


def gen1(camera):
    frame = cam.get_frame()
    yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def capture(request):
    try:
        cam.flag = False
        return StreamingHttpResponse(gen1(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

def recapture(request) :
    if request.method == 'POST':
        cam.flag = True
        threading.Thread(target=cam.update, args=()).start()
        pos = position.get_position()

        a = GuestBookModel.objects.get(id=position.get_position())
        try:
            b = GuestBookModel.objects.get(id = pos+1)
        except:
            b = None
        btn_up_visiable = position.next_page()
        btn_down_visiable = position.prev_page()
        detect = camera(cam)
        detect.start()

    return render(request,
                  'MaskGuestBook/index.html', {
                    'guest1' : a,
                    'guest2' : b,
                    'btn_up_visiable': btn_up_visiable,
                    'btn_down_visiable': btn_down_visiable})


def live(request):
    detect = camera(cam)
    detect.start()
    print("live")
    a = GuestBookModel.objects.get(id=position.get_position())
    b = GuestBookModel.objects.get(id=position.get_position() + 1)
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        message = request.POST['message']

        if(phone.isdigit()):
            cam.take_frame(name, phone, message)
        else:
            return render(request,
                          'MaskGuestBook/GuestBook.html',
                          {'error': "숫자만 입력해주세요",
                           'name' :name,
                           'message' : message
                           })

    return render(request,
                  'MaskGuestBook/index.html',
                  {'guest1' : a,
                   'guest2' : b,
                   'btn_up_visiable': False,
                    'btn_down_visiable': True})

position = position()

def next_page(request) :
    print('next_page')
    flag = True
    if request.method == 'GET':
        position.up()
        pos = position.get_position()
        a = GuestBookModel.objects.get(id = pos)
        try:
            b = GuestBookModel.objects.get(id = pos+1)
        except:
            b = None
        btn_up_visiable = position.next_page()
        btn_down_visiable = position.prev_page()

        print('next' + str(pos))
        return render(request,
                      'MaskGuestBook/index.html',
                      {'guest1': a,
                       'guest2': b,
                       'btn_up_visiable': btn_up_visiable,
                       'btn_down_visiable': btn_down_visiable})

def prev_page(request) :
    global position
    print('prev_page')
    flag = True
    if request.method == 'GET':
        position.down()
        pos = position.get_position()

        a = GuestBookModel.objects.get(id = pos)
        try:
            b = GuestBookModel.objects.get(id = pos+1)
        except:
            b = None
        btn_up_visiable = position.next_page()
        btn_down_visiable = position.prev_page()

        print(pos)
        return render(request,
                      'MaskGuestBook/index.html',
                      {'guest1': a,
                       'guest2': b,
                       'btn_up_visiable': btn_up_visiable,
                       'btn_down_visiable': btn_down_visiable})

