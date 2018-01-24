#!/usr/bin/env python

# install process
# sudo apt-get install python-pip
# sudo pip install google-cloud
# environment settings: open google cloud console:
# > API & Services > credentials> create credential > new service account > somename> role owner> json>downloadjason by click create
# rename it as apikey.json and keep it in a safe place
# gedit ~/.profile
# paste at end: export GOOGLE_APPLICATION_CREDENTIALS='/home/shaon/sdk/apikey.json' (the json path)
# source ~/.bashrc
# now run this python: python vision.py
# database set found at http://peipa.essex.ac.uk/benchmark/databases/index.html#faces

import io
import os

#imageNames = ['saurav.jpg', 'scenery.jpg','emotions.jpg','text.jpg']
dir_path = os.path.dirname(os.path.realpath(__file__))+'/resources/'

total_time=0.00


def run_vision(imageName):


    from google.cloud import vision
    from google.cloud.vision import types
    from datetime import datetime


    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(dir_path+imageName)


    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    start_time = datetime.now()
    global total_time
  #  total_time += start_time.total_seconds


    print('\n\n\n*******Analysis: '+imageName+'****************\n\n')

    image = types.Image(content=content)

    #label detection #####################################

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('\nLabels:\n')
    for label in labels:
        print(label.description)

    #face detection #######################################
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('\nFaces:\n')

    print('Number of Face found: '+str(len(faces)))

    for face in faces:
        #print('-------------------------------'+face)
        print('---')
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))

    # crop hints #############################################

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))


    # landmark ##############################################
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('\nLandmarks:\n')


    print('Number of Landmark found: '+str(len(landmarks)))

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude'.format(lat_lng.latitude))
            print('Longitude'.format(lat_lng.longitude))


    # text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('\nTexts:\n')


    print('Number of Text found: '+str(len(texts)))

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    timeNeeded = datetime.now() - start_time
    print('\n Time needed: '+ str(timeNeeded))

  #  global total_time
    total_time+=timeNeeded.total_seconds()
    print('\n Time total: ' + str(total_time))


if __name__ == '__main__':
    #run_vision('emotions.jpg')
#    for imageName in imageNames:
#        run_vision(imageName)


    imageNames= os.listdir(dir_path)
    print(imageNames)
    for imageName in imageNames:
        print('####'+str(imageName))
        run_vision(imageName)


    print('\n Total Time needed to analysis ' + str(len(imageNames)) + ' images: ' + str(total_time)+ ' seconds')