from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

#from .deca.demos import demo_reconstruct
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from os import path
from .models import Feedback
import random
import mimetypes
import urllib.request
import os.path
import shutil

# Create your views here.

selected_file=None
loc='constructor/static/images/'
uploc='constructor/static/uploads/'
obj_loc='constructor/deca/results/'
required=['.png','.jpg','.bmp','.mp4']

def upload(request):

    # global selected_file
    # selected_file=None

    # myfile = request.FILES['myfile'] if 'myfile' in request.FILES else False
    
    # if(request.method=='POST'):

    #     if(myfile!=False):
    #         _,ext=os.path.splitext(myfile.name)
        
    #         if(ext in required):

    #             selected_file=myfile.name
                
    #             if(path.exists(loc+selected_file)):
    #                 os.remove(loc+selected_file)

    #             fs = FileSystemStorage(location=loc)
    #             filename = fs.save(myfile.name, myfile)
    #             uploaded_file_url = fs.url(filename)

    #             try:
    #                 demo_reconstruct.main(loc+selected_file)
    #             except:
    #                 return render(request,'index.html')
                    
    #     return HttpResponseRedirect("/") 

    return HttpResponse('Upload Successful')

def cam_upload(request):
    # global selected_file
    # _,ext=os.path.splitext(selected_file)

    # if(ext in required):
    #     demo_reconstruct.main(loc+selected_file)
    return HttpResponseRedirect("/")

def cam(request):

    global selected_file
    if(selected_file!=None and path.exists(loc+selected_file)):
        os.remove(loc+selected_file)

    selected_file=None

    url = request.POST.get('url',None)

    if(url!=None): 

        filename="image"+str(random.randint(1,1000))+".png"
        urllib.request.urlretrieve(url, loc+filename)
        selected_file=filename
        print(selected_file)

    return HttpResponse('Cam Successful')

def lab(request):
    return HttpResponse('Lab Successful')

def viewer(request):
    return render(request,'viewer.html')

@csrf_exempt
def generate(request):

    if(request.method=='POST'):

        obj = request.FILES.get('obj') 
        mtl = request.FILES.get('mtl') 
        tex = request.FILES.get('tex') 

        if(obj and mtl and tex):
            name=os.path.splitext(obj.name)[0]
            upload=uploc+name+'/'
          
            try:
                shutil.rmtree(upload)
            except OSError as e:
                pass

            os.mkdir(upload)
            fs = FileSystemStorage(location=upload)
            obj = fs.save(obj.name, obj)
            mtl = fs.save(mtl.name, mtl)
            tex = fs.save(tex.name, tex)

            print(obj,mtl,tex)

            return HttpResponse(name+"/"+name) 

    return render(request,'viewer.html')

def home(request):
    global selected_file

    if(request.method=='POST'):
        if(request.POST.get('name') and request.POST.get('email') and request.POST.get('message')):
            fb=Feedback()
            fb.name= request.POST.get('name')
            fb.email= request.POST.get('email')
            fb.message= request.POST.get('message')
            fb.save()

    if(selected_file!=None):

        name,ext=selected_file.split('.')

        if(ext!="mp4"):

          file_name=name+'_detail.obj'

          det=name+'/'+file_name
          file_path = obj_loc+det

          file_wrapper = FileWrapper(open(file_path,'rb'))
          file_mimetype = mimetypes.guess_type(file_path)
          response = HttpResponse(file_wrapper, content_type=file_mimetype )
          response['X-Sendfile'] = file_path
          response['Content-Length'] = os.stat(file_path).st_size
          response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 

          selected_file=None

          return response

    return render(request,'index.html')
