import requests
import warnings
from tensorflow.keras import backend as K
import keras_unet
from tensorflow import keras
import tensorflow as tf
import png
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# Numerics
import nibabel as nib
import cv2
import numpy as np
import random
from PIL import Image as im
import random
import io

import glob
from PIL import Image
import pydicom

# Visuals
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tqdm import tqdm
from django.template.defaulttags import register


# Env
import os
from os import path
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = ''

# Backend
# import keras
warnings.filterwarnings("ignore")


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


def CovidHome(request):
    userFile = request.user
    # print(userFile)
    outputdir = 'media/covidFiles/' + str(userFile) + '/'
    isDir = os.path.isdir(outputdir)
    if (isDir == False):
        os.mkdir(outputdir)
    dcm_folder = outputdir + "DCM_Folder" + "/"
    is_dcm = os.path.isdir(dcm_folder)
    if(is_dcm == False):
        os.mkdir(dcm_folder)
    predicted_folder = outputdir + "Predicted_Folder" + "/"
    is_predicted = os.path.isdir(predicted_folder)
    if(is_predicted == False):
        os.mkdir(predicted_folder)
    return render(request, 'covidct/Covid_Home.html')


@login_required(login_url='/auth/login')
def uploadCovid(request):
    userFile = request.user
    outputdir = 'media/covidFiles/' + str(userFile) + '/DCM_Folder/'
    if(request.method == 'POST'):
        imgName = request.FILES['covid_document']
        # print(imgName.name)
        fs = FileSystemStorage(location=outputdir, base_url=outputdir)
        x = fs.save(imgName.name, imgName)
        filename = Convert_To_PNG(x, userFile)
        # os.remove(outputdir + x)
        context['url'] = fs.url(filename)
        # print(context['url'])
    return render(request, 'covidct/upload_Covid.html')


def Convert_To_PNG(dcmFile, username):
    file = dcmFile
    context = {}
    userFile = username
    inputdir = 'media/covidFiles/' + str(userFile) + '/DCM_Folder/'
    outputdir = 'media/covidFiles/' + str(userFile) + '/DCM_Folder/'
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


@login_required(login_url='/auth/login')
def getCovidList(request):
    userFile = request.user
    if userFile.is_superuser:
        cl = {}
        for (root, dirs, files) in os.walk('media/covidFiles'):
            for i in files:
                # dir_list.append(i)
                # dir=os.path.join(root,i)
                dir_list = os.listdir(root)
                for dimg in dir_list:
                    covidList = {}
                    tmpFile = dimg
                    if(tmpFile.endswith('.dcm')):
                        filename = root + "/" + tmpFile
                        dataset = pydicom.dcmread(filename)
                        y = dataset.data_element("PatientID").value
                        covidList["PatientID"] = y
                        x = dataset.data_element("PatientName").value
                        covidList["PatientName"] = x
                        covidList["PatientSex"] = dataset.data_element(
                            "PatientSex").value
                        covidList["PatientAge"] = dataset.data_element(
                            "PatientAge").value
                        covidList["StudyDate"] = dataset.data_element(
                            "StudyDate").value
                        covidList["Modality"] = dataset.data_element(
                            "Modality").value
                        covidList["ImageComments"] = dataset.data_element(
                            "ImageComments").value
                        covidList["SeriesDescription"] = dataset.data_element(
                            "SeriesDescription").value
                        covidList["BodyPartExamined"] = dataset.data_element(
                            "BodyPartExamined").value
                        covidList["User"] = root.split("/")[-2]
                        cl[dimg] = covidList
        return render(request, "covidct/listCovid.html", {"cl": cl})

    else:
        cl = {}
        outputdir = "media/covidFiles/" + str(userFile) + "/DCM_Folder/"
        isDir = os.path.isdir(outputdir)
        if (isDir == False):
            os.mkdir(outputdir)
        # cl = {}
        dir = outputdir
        dir_list = os.listdir(dir)
        for dimg in dir_list:
            covidList = {}
            tmpFile = dimg
            if(tmpFile.endswith('.dcm')):
                filename = dir + tmpFile
                dataset = pydicom.dcmread(filename)
                y = dataset.data_element("PatientID").value
                covidList["PatientID"] = y
                x = dataset.data_element("PatientName").value
                covidList["PatientName"] = x
                covidList["PatientSex"] = dataset.data_element("PatientSex").value
                covidList["PatientAge"] = dataset.data_element("PatientAge").value
                covidList["StudyDate"] = dataset.data_element("StudyDate").value
                covidList["Modality"] = dataset.data_element("Modality").value
                covidList["ImageComments"] = dataset.data_element(
                    "ImageComments").value
                covidList["SeriesDescription"] = dataset.data_element(
                    "SeriesDescription").value
                covidList["BodyPartExamined"] = dataset.data_element(
                    "BodyPartExamined").value
                covidList["User"] = str(userFile)
                cl[dimg] = covidList
        return render(request, "covidct/listCovid.html", {"cl": cl})


def dcm_to_png(dcmFile, username):
    file = dcmFile
    context = {}
    userFile = username
    inputdir = 'media/covidFiles/' + str(userFile) + '/'
    outputdir = 'media/covidFiles/' + str(userFile) + '/'
    test_list = [os.path.basename(x) for x in glob.glob(inputdir + '*.dcm')]
    # print(test_list)
    for f in test_list:
        if(f == file):
            ds = pydicom.read_file(inputdir + file)
            image_2d = ds.pixel_array
            shape = ds.pixel_array.shape
            image_2d_scaled = (np.maximum(image_2d, 0) /
                               image_2d.max()) * 255.0
            image_2d_scaled = np.uint8(image_2d_scaled)

            png_file_name = outputdir + "/predicted-" + file[:-4] + ".png"

            with open(png_file_name, 'wb') as png_file:
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(png_file, image_2d_scaled)


def predictSpecificImage(request):
    return 0

# @login_required(login_url='/auth/login')
# def uploadToServer(request):
#     if(request.method == 'POST'):
#         fs = FileSystemStorage(location="media/covidFiles/", base_url="media/covidFiles/")
#         toup = request.FILES['filetoupload']
#         print(toup.name)
#         fdict = { 'image' : toup }
#         resp = requests.post("http://localhost:1111/fileupload", data = fdict);
#         # print(resp.status_code)
#     return render(request, 'covidct/upload_Covid.html')


context = {}
imgDict = {}


@login_required(login_url='/auth/login')
def predictCovid(request):
    userFile = request.user
    if userFile.is_superuser:
        cl = {}
        for (root, dirs, files) in os.walk('media/covidFiles'):
            for i in files:
                dir_list = os.listdir(root)
                for dimg in dir_list:
                    covidList = {}
                    tmpFile = dimg
                    if(tmpFile.endswith('.dcm')):
                        filename = root + "/" + tmpFile
                        dataset = pydicom.dcmread(filename)
                        y = dataset.data_element("PatientID").value
                        covidList["PatientID"] = y
                        x = dataset.data_element("PatientName").value
                        covidList["PatientName"] = x
                        covidList["User"] = root.split("/")[-2]
                        covidList["FileName"] = tmpFile
                        cl[dimg] = covidList
        outputdir = "media/covidFiles/" + str(userFile) + "/Predicted_Folder/"
        if (request.method == 'POST'):
            if userFile.is_superuser:
                userstmp = {}
                for (root, dirs, files) in os.walk('media/covidFiles'):
                    for i in files:
                        dir_list = os.listdir(root)
                        for dimg in dir_list:
                            userDict = {}
                            userDict["User"] = root.split("/")[-2]
                            userstmp[dimg] = userDict
            fs = FileSystemStorage(
                location=outputdir, base_url=outputdir)
            img = request.FILES['doc1']
            ims = fs.save(img.name, img)
            imgUrl = fs.url(ims)
            predicted_img = get_display_image(imgUrl)
            data = im.fromarray(predicted_img)
            rr = random.randint(0, 99)
            predicted_Image_name = 'predicted' + str(rr) + '.png'
            imgDict["predicted_Image_name"] = predicted_Image_name
            data.save(outputdir + predicted_Image_name)
            os.remove(outputdir + ims)
            MainUsersList = []
            for i in userstmp.values():
                for mainUsers in i.values():
                    if mainUsers not in MainUsersList:
                        MainUsersList.append(mainUsers)
            return render(request, 'covidct/predict_Covid.html', {'url': predicted_Image_name, "MainUsersList": MainUsersList, 'currUser': userFile})
    return render(request, 'covidct/predict_Covid.html', {"cl": cl})


def showCovid(request):
    return render(request, 'covidct/showPredicted.html')


def sentImage(request):
    isSent = False
    if(request.method == 'POST'):
        toSend = request.POST.get('checkedUser')
        saveDir = "media/covidFiles/" + str(toSend) + "/Predicted_Folder/"
        retrieveDir = "media/covidFiles/" + "admin" + "/Predicted_Folder/"
        fs = FileSystemStorage(
            location=saveDir, base_url=saveDir)
        predictedImage = imgDict["predicted_Image_name"]
        for f in os.listdir(retrieveDir):
            if(f == predictedImage):
                isSave = cv2.imread(retrieveDir + predictedImage)
                data = im.fromarray(isSave)
                data.save(saveDir + f)
                isSent = True
        return render(request, 'covidct/predict_Covid.html', {'isSent': isSent, 'toSend' : toSend})
    return render(request, 'covidct/predict_Covid.html', {'isSent': isSent})
# Predictions


WEIGHTS_PATH = 'covid/model_png.h5'


def dice_coef(y_true, y_pred, smooth=1):
    smooth = 1e-7
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    return (2. * intersection + smooth) / (K.sum(K.square(y_true), -1) + K.sum(K.square(y_pred), -1) + smooth)


def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)


def soft_dice_loss(y_true, y_pred, epsilon=1e-6):
    axes = tuple(range(1, len(y_pred.shape)-1))
    numerator = 2. * np.sum(y_pred * y_true, axes)
    denominator = np.sum(np.square(y_pred) + np.square(y_true), axes)
    return 1 - np.mean((numerator + epsilon) / (denominator + epsilon))


def calc_loss(y_true, y_pred):
    bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)
    dice = dice_coef_loss(y_true, y_pred)
    return 0.4 * bce + 0.6 * dice

#-------------------------------------------------------------------------------#


def load_model():
    model = keras_unet.models.custom_unet((624, 624, 1), 1)

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=calc_loss,
                  metrics=['accuracy', dice_coef, tf.keras.metrics.MeanIoU(num_classes=2)])

    model.load_weights(WEIGHTS_PATH)
    return model


def predict(img):
    img = cv2.imread(img, 0)
    img = cv2.resize(img, (624, 624),
                     interpolation=cv2.INTER_NEAREST)
    #print("------------------------- Image shape -------------------------: " , img.shape)
    img = np.array(img, dtype=np.float32)

    Max = np.amax(img)
    Min = np.amin(img)
    #print("------------------------- Image Min -------------------------: ", Max, Min);
    off_set = Max - Min
    img = img.copy()
    img += abs(Min)
    img /= off_set
    img *= 255.0

    img /= 255.0

    img = np.expand_dims(img, 2)

    img = np.expand_dims(img, 0)

    model = load_model()
    pred = model.predict(img)
    pred = cv2.threshold(pred[0], 0.2, 1, cv2.THRESH_BINARY)[1]
    # msk = msk[0][:, :, 0]
    # acc = np.sum(pred == msk)/(624*624)
    pred *= 255
    # acc *= 100
    return pred


def get_display_image(img):
    # print(img)
    pred_ = predict(img)
    img = cv2.imread(img, 1)
    img = cv2.resize(img, (624, 624),
                     interpolation=cv2.INTER_NEAREST)
    #img = np.array(img, dtype=np.float32)
    # Max = np.amax(img)
    # Min = np.amin(img)

    # off_set = Max - Min
    # img = img.copy()
    # img += abs(Min)
    # img /= off_set
    # img *= 255.0
    # msk = cv2.imread(msk, 1)

    # gt = msk.copy()
    # gt[:, :, [0, 2]] = 0
    # gt = cv2.addWeighted(img, 0.8, gt, 0.2, 0)

    pred = np.zeros((624, 624, 3), dtype=np.uint8)
    pred[:, :, 0] = pred_
    pred = cv2.addWeighted(img, 0.8, pred, 0.2, 0)

    # fh = 30
    # fw = 15
    # imgs = [img, pred]
    # titles = ['Original', 'Ground Truth Borders (Expert-annotated)', 'Predicted Borders ( Accuracy : ' + "{:.2f})".format(acc)]
    # f, ax = plt.subplots(1, len(imgs), figsize=(fh,fw))
    # for i in range(len(imgs)):
    #     ax[i].imshow(imgs[i])
    #     if titles is not None:
    #         ax[i].title.set_text(titles[i])
    #         ax[i].title.set_size(20)

    # canvas = FigureCanvas(f)
    # canvas.draw()
    # ret = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(fw*100, fh*100, 3)
    # return ret
    fh = 30
    fw = 15
    imgs = [img, pred]
    titles = ['Original', 'Covid Region']
    f, ax = plt.subplots(1, len(imgs), figsize=(fh, fw))
    for i in range(len(imgs)):
        ax[i].imshow(imgs[i])
        if titles is not None:
            ax[i].title.set_text(titles[i])
            ax[i].title.set_size(20)

    canvas = FigureCanvas(f)
    canvas.draw()
    ret = np.frombuffer(canvas.tostring_rgb(),
                        dtype='uint8').reshape(fw*100, fh*100, 3)
    return ret
