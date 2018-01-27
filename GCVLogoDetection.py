
import io
import os

dir_path = os.path.dirname(os.path.realpath(__file__))+'/resources/logodataset/100logos/'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()
noOfTotalLogo =0


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

    #Logo detection #####################################

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('\nLogos:\n')

    print('Number of Logo found: ' + str(len(logos)))
    global noOfTotalLogo
    noOfTotalLogo = noOfTotalLogo + len(logos)

    print('\n Result: ')
    if (len(logos) == 0):
        print('\nNo Logo Found')
        notFoundList.append(imageName)
        return

    success= success+1

    for logo in logos:
        print(logo.description)

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

    print('\n\n\n *************** Analysis Details: '+imageTitle+' *************')
    print('\n Number of Image: '+ str(len(imageNames)))

    print('success rate: ' + str(success * 100 / noOfImages) + '%')
    print('\n Total Time needed to analysis ' + str(len(imageNames)) + ' images: ' + str(total_time)+ ' seconds, \n  Average: '+str(total_time/len(imageNames)) + ' Sec/image')
    print ('\n Not Found Image list '+ str(notFoundList))
