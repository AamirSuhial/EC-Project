
import io
import os

#imageNames = ['saurav.jpg', 'scenery.jpg','emotions.jpg','text.jpg']
imageTitle='barrel'
dir_path = os.path.dirname(os.path.realpath(__file__))+'/resources/objectdataset/'+imageTitle+'/'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()


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

    #label detection #####################################

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('\nLabels:\n')
    found = 0
    for label in labels:
        print(label.description)
        if(label.description==imageTitle):
            success +=1
            found = 1


    print('\n Result: ')
    if(found == 0):
        print('\n Not Found ' + imageTitle + ' in ' + imageName)
        notFoundList.append(imageName)
    else:
        print('\n Match Found')

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
    print ('\n Found '+ imageTitle + ' in image: ' + str(success) + ' times')
    print('success rate: ' + str(success * 100 / noOfImages) + '%')
    print('\n Total Time needed to analysis ' + str(len(imageNames)) + ' images: ' + str(total_time)+ ' seconds, \n  Average: '+str(total_time/len(imageNames)) + ' Sec/image')
    print ('\n Not Found Image list '+ str(notFoundList))
