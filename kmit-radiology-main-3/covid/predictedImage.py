#Numerics
import nibabel as nib
import cv2
import numpy as np
import random

#Visuals
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tqdm import tqdm

#Env
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = ''

#Backend
import tensorflow as tf
import keras
import keras_unet
from keras import backend as K

WEIGHTS_PATH = './model_png.h5'
#-------------------------------------------------------------------------------#
def dice_coef(y_true, y_pred, smooth=1):
    smooth = 1e-7
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    return (2. * intersection + smooth) / (K.sum(K.square(y_true),-1) + K.sum(K.square(y_pred),-1) + smooth)

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)

def soft_dice_loss(y_true, y_pred, epsilon=1e-6): 
    axes = tuple(range(1, len(y_pred.shape)-1)) 
    numerator = 2. * np.sum(y_pred * y_true, axes)
    denominator = np.sum(np.square(y_pred) + np.square(y_true), axes) 
    return 1 - np.mean((numerator + epsilon) / (denominator + epsilon))

def calc_loss(y_true, y_pred):
    bce = keras.losses.binary_crossentropy(y_true, y_pred)
    dice = dice_coef_loss(y_true, y_pred)
    return 0.4 * bce + 0.6 * dice

#-------------------------------------------------------------------------------#
def load_model():
    model = keras_unet.models.custom_unet((624, 624, 1), 1)

    model.compile(optimizer=keras.optimizers.Adam(), 
                loss=calc_loss, 
                metrics=['accuracy', dice_coef, tf.keras.metrics.MeanIoU(num_classes=2)])

    model.load_weights(WEIGHTS_PATH)
    return model

def predict(img, msk):
    img = cv2.imread(img, 0)
    msk = cv2.imread(msk, 0)

    img = np.array(img, dtype=np.float32)
    msk = np.array(msk, dtype=np.float32)

    img /= 255.0
    msk /= 255.0

    img = np.expand_dims(img, 2)
    msk = np.expand_dims(msk, 2)

    img = np.expand_dims(img, 0)
    msk = np.expand_dims(msk, 0)

    model = load_model()
    pred = model.predict(img)
    pred = cv2.threshold(pred[0], 0.2, 1, cv2.THRESH_BINARY)[1]
    msk = msk[0][:, :, 0]
    acc = np.sum(pred == msk)/(624*624)
    pred *= 255
    acc *= 100
    return acc, pred

def get_display_image(img, msk):
    acc, pred_ = predict(img, msk)
    img = cv2.imread(img, 1)
    msk = cv2.imread(msk, 1)
    
    gt = msk.copy()
    gt[:, :, [0, 2]] = 0
    gt = cv2.addWeighted(img, 0.8, gt, 0.2, 0)

    pred = np.zeros((624, 624, 3), dtype=np.uint8)
    pred[:, :, 0] = pred_
    pred = cv2.addWeighted(img, 0.8, pred, 0.2, 0)

    fh = 30
    fw = 15
    imgs = [img, gt, pred]
    titles = ['Original', 'Ground Truth Borders (Expert-annotated)', 'Predicted Borders ( Accuracy : ' + "{:.2f})".format(acc)]
    f, ax = plt.subplots(1, len(imgs), figsize=(fh,fw))
    for i in range(len(imgs)):
        ax[i].imshow(imgs[i])
        if titles is not None:
            ax[i].title.set_text(titles[i])
            ax[i].title.set_size(20)

    canvas = FigureCanvas(f)
    canvas.draw()
    ret = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(fw*100, fh*100, 3)
    return ret
