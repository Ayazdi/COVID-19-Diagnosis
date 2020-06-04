# COVID-19-Diagnosis
**A web base engine to diagnose COVID-19 by CT scans**

COVID-19 has infected more than 6 million people worldwide so far, and this number is still increasing drastically. The crucial fast approach to control the spread is testing large number of individuals. Thus, rapid diagnosis of the virus infection via CT scan images has been wildly used in many countries. This project utilizes **Computer Vision** to detect COVID-19 infection in the chest CT scan images of the patients with a highly accurate model.

![screenshot](/Screenshot_1.png)
![screenshot](/Screenshot_2.png)

## Model
The diagnosis model was obtained by the fine-tuning Inception_V3 model and Keras image data generator using "covid-19-x-ray-10000-images dataset" from kaggle. The external validation on the test data achieved a total accuracy of 97% with average specificity of 98% and sensitivity of 94%.

Step-by-step description of the model training is included in model.ipynb

## Dataset

- https://www.kaggle.com/nabeelsajid917/covid-19-x-ray-10000-images
- Arad Hospital, Tehran, Iran dataset (soon to be added)


## Tech used:
- Python
- TensorFlow
- Paperspace
- Inception-V3
- Flask

## Usage:
1. Install the requirements

2. Clone this repository: git clone
`https://github.com/Ayazdi/COVID-19-Diagnosis`

3. Run run_web.sh and go the provided link in your browser(localhost:5000)


## Contacts:
https://www.linkedin.com/in/amirali-yazdi-872b5460/

## Future works
 - Upload the website via Heroku
 - Docker containerize the project
 - Train a model to diagnose with symptoms and add it to the website
 - Train a model to diagnose with other medical data
 - Add CT scan images from Arad Hospital, Tehran, Iran and retrain the model

## License
Free software: MIT License
