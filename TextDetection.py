
import io
import os

dir_path = os.path.dirname(os.path.realpath(__file__))+'/resources/textdataset/text/'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()
noOfTotalText =0


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

    #
    # text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('\nTexts:\n')

    print('Number of Text found: ' + str(len(texts)))
    global noOfTotalText
    noOfTotalText = noOfTotalText + len(texts)

    print('\n Result: ')
    if (len(texts) == 0):
        print('\nNo Text Found')
        notFoundList.append(imageName)
        return

    success = success + 1

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

#        print('bounds: {}'.format(','.join(vertices)))


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
    #run_vision('img491.jpg')

    print('\n\n\n *************** Analysis Details: '+imageTitle+' *************')
    print('\n Number of Image: '+ str(len(imageNames)))

    print('success rate: ' + str(success * 100 / noOfImages) + '%')
    print('\n Total Time needed to analysis ' + str(len(imageNames)) + ' images: ' + str(total_time)+ ' seconds, \n  Average: '+str(total_time/len(imageNames)) + ' Sec/image')
    print ('\n Not Found Image list '+ str(notFoundList))
