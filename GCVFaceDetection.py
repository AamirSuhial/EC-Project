
import io
import os

#imageNames = ['saurav.jpg', 'scenery.jpg','emotions.jpg','text.jpg']

dir_path = os.path.dirname(os.path.realpath(__file__))+'/resources/facedataset/s2/'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()
noOfTotalFace = 0


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


    print('\n*******Analysis: '+imageName+'****************\n\n')

    image = types.Image(content=content)
    global success

    # face detection #######################################
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('\nFaces:\n')

    print('Number of Face found: ' + str(len(faces)))
    global noOfTotalFace
    noOfTotalFace = noOfTotalFace + len(faces)

    print('\n Result: ')
    if (len(faces) == 0):
        print('\nNo Face Found')
        notFoundList.append(imageName)
        return

    for face in faces:
        # print('-------------------------------'+face)
        print('---')
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))



    timeNeeded = datetime.now() - start_time
    print('\n Time needed: '+ str(timeNeeded))

  #  global total_time
    total_time+=timeNeeded.total_seconds()
    print('\n Time total: ' + str(total_time) + ' Sec')


if __name__ == '__main__':

    imageNames= os.listdir(dir_path)
    noOfImages=len(imageNames)
    print('no of images: '+ str(noOfImages))
    for imageName in imageNames:
        run_vision(imageName)

    print('\n\n\n *************** Analysis Details:  *************')
    print('\n Number of Image: '+ str(len(imageNames)))
    print ('\n No of Face found: ' + str(noOfTotalFace) + ' times')
    # case s1 face per image
    print('success rate: ' + str(noOfTotalFace * 100 / (20*20)) + '%')
    #case s2 face per image
    #print('success rate: ' + str(noOfTotalFace * 100 / noOfImages) + '%')
    print('\n Total Time needed to analysis ' + str(len(imageNames)) + ' images: ' + str(total_time)+ ' seconds, \n  Average: '+str(total_time/len(imageNames)) + ' Sec/image')
    print ('\n Not Found Image list '+ str(notFoundList))
