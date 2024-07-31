from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import cv2
import os
import pydicom
import glob
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Predicting Mammograms
#from .frcnn_test_vgg import predictt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def MammoHome(request):
    #print(request.user)
    return render(request, 'mammo/MammoHome.html')


filename = "lol"
context = {}


def uploadMammo(request):
    userFile = request.user
    outputdir = 'media/mammoFiles/' + str(userFile) + '/'
    isDir = os.path.isdir(outputdir)
    if (isDir == False):
        os.mkdir(outputdir)
    
    if(request.method == 'POST'):
        imgName = request.FILES['Mammo_doc']
        #print(imgName.name)
        fs = FileSystemStorage(location=outputdir, base_url=outputdir)
        x = fs.save(imgName.name, imgName)
        filename = Convert_To_PNG(x, userFile)
        # os.remove(outputdir + x)
        context['url'] = fs.url(filename)
        #print(context['url'])
        return render(request, 'mammo/upload_Mammo.html', {'stored' : True})
    return render(request, 'mammo/upload_Mammo.html')

# def uploadMammo(request):
#     outputdir = 'media/'
#     if (request.method == 'POST'):
#         uploaded_file = request.FILES['document']
#         upName = uploaded_file.name
#         if(upName.lower().endswith('.dcm')):
#             fs = FileSystemStorage()
#             x = fs.save(uploaded_file.name, uploaded_file)
#             filename = Convert_To_PNG(x)
#             os.remove(outputdir + x)
#             context['url'] = fs.url(filename)
#             # print(context['url'])
#         else:
#             fs = FileSystemStorage()
#             filename = fs.save(uploaded_file.name, uploaded_file)
#             context['url'] = fs.url(filename)
#             # print(outputdir + x)
#     return render(request, 'mammo/uploadMammo.html', context)


def Convert_To_PNG(dcmFile, username):
    file = dcmFile
    context = {}
    userFile = username
    inputdir = 'media/mammoFiles/' + str(userFile) + '/'
    outputdir = 'media/mammoFiles/' + str(userFile) + '/'
    test_list = [os.path.basename(x) for x in glob.glob(inputdir + '*.dcm')]
    # print(test_list)
    for f in test_list:
        if(f == file):
            ds = pydicom.read_file(inputdir + f)
            img = ds.pixel_array
            cv2.imwrite(outputdir + f.replace('.dcm', '.png'), img)
    out_list = [os.path.basename(x) for x in glob.glob(inputdir + '*.png')]
    for name in out_list:
        if(name[:-4] == file[:-4]):
            return name

# @login_required(login_url='/auth/login')
def predictMammo(request):
    outputdir = 'media/mammoFiles/'
    if (request.method == 'POST'):
        fs = FileSystemStorage(location="media/mammoFiles/", base_url="media/mammoFiles/")
        img = request.FILES['mammoDoc']
        ims = fs.save(img.name, img)
        imgUrl = fs.url(ims)
        #print(imgUrl)
        inp = np.array(Image.open(img))
        #print(imgUrl.split('/')[-1])
        # pred = predictt(inp, imgUrl.split("/")[-1])
        # print(pred.shape)
    return render(request, 'mammo/predictMammo.html')
