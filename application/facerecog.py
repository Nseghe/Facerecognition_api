import numpy as np
import os
import cv2
from imageio import imread
import matplotlib.pyplot as plt
from skimage.transform import resize
from scipy.spatial import distance
from keras.backend import set_session
from keras.models import load_model
import tensorflow as tf
from mtcnn import MTCNN
import glob
from PIL import Image
from io import BytesIO
import base64

sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()
set_session(sess)

model = load_model('./application/model/facenet_keras.h5', compile=False)
image_size = 160


def predict(img):
    global graph
    global sess
    with graph.as_default():
        set_session(sess)
        result = model.predict_on_batch(img)
    return result


def read_image(data):
    # _, encoded = data.split(",", 1)
    encoded = data
    im = Image.open(BytesIO(base64.b64decode(encoded)))
    return np.array(im)
def prewhiten(x):
    if x.ndim == 4:
        axis = (1, 2, 3)
        size = x[0].size
    elif x.ndim == 3:
        axis = (0, 1, 2)
        size = x.size
    else:
        raise ValueError('Dimension should be 3 or 4')

    mean = np.mean(x, axis=axis, keepdims=True)
    std = np.std(x, axis=axis, keepdims=True)
    std_adj = np.maximum(std, 1.0/np.sqrt(size))
    y = (x - mean) / std_adj
    return y

def l2_normalize(x, axis=-1, epsilon=1e-10):
    output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
    return output

def load_and_align_images(data, margin):
    detector = MTCNN()
    
    aligned_images = []
    img = read_image(data)

    faces = detector.detect_faces(img)
    (x, y, w, h) = faces[0]['box']
    
    cropped = img[y-margin//2:y+h+margin//2,
                  x-margin//2:x+w+margin//2, :]
    aligned = resize(cropped, (image_size, image_size), mode='reflect')
    aligned_images.append(aligned)
            
    return np.array(aligned_images)

def calc_embs(data, margin=10, batch_size=1):
    aligned_images = prewhiten(load_and_align_images(data, margin))
    pd = []
    for start in range(0, len(aligned_images), batch_size):
        pd.append(predict(aligned_images[start:start+batch_size]))
    embs = l2_normalize(np.concatenate(pd))

    return embs

def calc_dist(image1, image2):# pair):
    # data = [None]*2
    # for i in range(len(pair)):
    #   img_data = pair[i] 
    #   embs = calc_embs(img_data)
    #   data[i] = embs
    data = [calc_embs(image1), calc_embs(image2)]
    return distance.euclidean(data[0], data[1])

def calc_dist_plot(pair):
    print(calc_dist(pair))
    plt.subplot(1, 2, 1)
    plt.imshow(imread(pair[0]))
    plt.subplot(1, 2, 2)
    plt.imshow(imread(pair[1]))
    
