import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image
import urllib.request
import numpy as np


def load_logo_model(model):
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


model = load_logo_model('model_2')


def logo_detection(image):
    """
    Detects the infection in the chest CT scan image

    image: CT scan image

    return: dignosis result (str)
    """
    # load image from the url
    img = Image.open(image)

    # trasnform to a desireable tensor for the model
    img = img.resize((224, 224), Image.ANTIALIAS)

    x = img_to_array(img)/255.
    x = x.reshape((1,) + x.shape)

    # prediction
    result = model.predict(x)
    prediction = np.argmax(result)

    if prediction == 0:
        prediction = 'covid'
    else:
        prediction = 'normal'

    return prediction
