import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image
import cv2
import urllib.request
import numpy as np


def load_model(model):
    """
    load the saved trained model
    """
    # logging.critical("Loading logo detection model...")
    json_file = open(f'{model}.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(f"{model}.h5")
    # logging.critical("Model is ready.")
    return loaded_model


model = load_model('model_2')


def ct_scan_diagnosis(image):
    """
    Detects the infection in the chest CT scan image

    image: CT scan image

    return: dignosis result (str)
    """
    # img = Image.open(image)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, (224, 224))

    # # load image from the url
    img = Image.open(image)
    img = img.convert('RGB')

    # trasnform to a desireable tensor for the model
    img = img.resize((224, 224), Image.ANTIALIAS)

    x = img_to_array(img)/255.
    print(x.shape)
    x = x.reshape((1,) + x.shape)
    print(x.shape)

    # prediction
    result = model.predict(x)
    prediction = np.argmax(result)

    if prediction == 0:
        prediction = 'COVID-19'
    else:
        prediction = 'Normal'

    return prediction


if __name__ == '__main__':
    predic = ct_scan_diagnosis('./uploads/normal_22.jpeg')
    print(predic)
