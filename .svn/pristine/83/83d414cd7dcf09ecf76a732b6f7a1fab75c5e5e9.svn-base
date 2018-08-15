from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.generic import TemplateView
import cv2 as cv
import base64
import re
import numpy as np
from django.core.files.base import ContentFile
import sys
from .services import ImageProcess, Common
from django.conf import settings
import glob, mimetypes, os
from .models import Image

PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

def index(request):
    if request.method == 'POST' and 'imageData' in request.POST:   

        imageData = request.POST.get('imageData')
        format, imgstr = imageData.split(';base64,') 
        
        #ext of file
        ext = format.split('/')[-1] 

        message = ""
        # If none or len 0, means illegal image data
        if imgstr == None or len(imgstr) == 0:
            # PRINT ERROR MESSAGE HERE
            message= "画像ファイルが存在しません。"

        # Decode the 64 bit string into 32 bit
        data = base64.b64decode(imgstr)
        fs = FileSystemStorage()

        #save file
        fileName = request.POST.get('fileName') + "_template." + ext
        fs.save(fileName, ContentFile(data))

        #save database 
        coordinateStr = request.POST.get('coordinateStr')

        if Image.objects.filter(image_name = fileName).exists():
            Image.objects.filter(image_name=fileName).delete()
        record = Image(image_name=fileName, image_coordinates=coordinateStr)
        record.save()    

        return JsonResponse({'message':message})

    return render(request, 'pages/home.html')

def resize(request):
    return render(request, 'pages/resize.html')


def areaOfShape(request):
    if request.method == 'POST' and 'imageData' in request.POST:   
        imageData = request.POST.get('imageData')
        format, imgstr = imageData.split(';base64,') 
      
        message = ""
        # If none or len 0, means illegal image data
        if imgstr == None or len(imgstr) == 0:
            # PRINT ERROR MESSAGE HERE
            message= "画像ファイルが存在しません。"

        # Decode the 64 bit string into 32 bit
        data = base64.b64decode(imgstr)        
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv.imdecode(image, cv.IMREAD_COLOR)

        contour = find_contour(image,  request.POST.get('clickX'),  request.POST.get('clickY'))
        x,y,w,h = cv.boundingRect(contour)
        
    return JsonResponse({'x':x,'y':y,'w':w,'h':h})
    
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_contour(img, clickX, clickY):
    minimum = 0
    img = cv.GaussianBlur(img, (5, 5), 0)
    contour=[]
    for gray in cv.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv.Canny(gray, 0, 50, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                    if cv.pointPolygonTest(cnt, (float(clickX), float(clickY)), True) >= 0 and \
                      (minimum == 0 or cv.contourArea(cnt) < minimum) :
                        minimum = cv.contourArea(cnt)
                        contour = cnt
    return contour

class CoincideImages(TemplateView):
    template_name = 'pages/CoincideImages.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CoincideImages, self).get_context_data(*args, **kwargs)
        tmpl_lst = list(map(lambda x: os.path.basename(x),glob.glob("%s/*.*" %settings.MEDIA_ROOT)))
        context['tmpl_lst'] = tmpl_lst
        return context

def GetCorrectImage(request):
    if request.method == 'POST':
        rp_img_stream = request.FILES['report'].file
        tmpl_img_name = request.POST['template-name']
        tmpl_img_path = os.path.join(settings.MEDIA_ROOT, tmpl_img_name)
        tmpl_img_stream = open(tmpl_img_path, 'rb')

        try:
            crt_img_stream = ImageProcess.correctImage(tmpl_img_stream, rp_img_stream)
            response = HttpResponse(crt_img_stream, content_type='image/png')
            return response
        except ArithmeticError as e:
            return HttpResponseServerError(e.args)
        except Exception:
            return HttpResponseServerError("CorrectImageができません。")
            
def GetTemplate(request):
    if request.method == 'GET':
        file_name = request.GET['file-path']

        try:
            img_coords_str = list(Image.objects.filter(image_name=file_name).values_list('image_coordinates', flat=True))[0]
            response = {}
            response['img-coords'] = Common.ConvertCoordsAPI(img_coords_str)
            response['tmpl-img'] = os.path.join(settings.MEDIA_URL, file_name)
            return JsonResponse(response)
        except IOError:
            return HttpResponseServerError("テンプレートが見つかりません。")
        except Exception as e:
            return HttpResponseServerError(e.args)
