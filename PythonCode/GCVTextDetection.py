
import io
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))+'/resources/textdataset/text20/'
textDB_path = os.path.dirname(os.path.realpath(__file__))+'/resources/textdataset/text20database/'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()
noOfTotalText =0
totalWordsinDB = 0
totalMatch = 0



def run_vision(imageName,dbName):


    from google.cloud import vision
    from google.cloud.vision import types
    from datetime import datetime


    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(dir_path+imageName)
    db_name = os.path.join(textDB_path + str(dbName)+'.txt')


    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    with open(db_name, 'r') as dbfile:
        dataStr = dbfile.read().replace('\n', '')

    dataArray= dataStr.split(',')
    global totalWordsinDB
    totalWordsinDB = totalWordsinDB + len(dataArray)

    start_time = datetime.now()
    global total_time
  #  total_time += start_time.total_seconds


    print('\n*******Analysis: '+imageName+'****************\n\n')

    image = types.Image(content=content)
    global success
    match = 0
    foundWord = list()

    try:
    #
    # text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations
        #print('\nTexts:\n')

        print('Number of Text found: ' + str(len(texts)))
        global noOfTotalText
        noOfTotalText = noOfTotalText + len(texts)

        print('\n Result: ')
        if (len(texts) == 0):
            print('\nNo Text Found')
            notFoundList.append(imageName)
            return

        success = success + 1
        print('Text Detected: ')
        for text in texts:
            print(text.description)

        for text in texts:
            #print('\n------------- compare: ' + format(text.description))
            for data in dataArray:
                #print('Compare: ' + text.description + ' and ' + data)
                if(text.description.upper()==data.upper()):
                    #print('Match found: ' + text.description + ' with ' + data)
                    foundWord.append(text.description)
                    match=match+1
                    global totalMatch
                    totalMatch = totalMatch+1
           # print('\n"{}"'.format(text.description))

            #vertices = (['({},{})'.format(vertex.x, vertex.y)
            #             for vertex in text.bounding_poly.vertices])

    #        print('bounds: {}'.format(','.join(vertices)))

    except:
        e = sys.exc_info()[0]
        print('exception throw: '+ str(e))
        notFoundList.append(imageName)

    print('\n\n --- Analysis for this image')

    print('\nWords in DB: '+ str(len(dataArray)))
    print('Match found: '+ str(match)+ ' ----------------------------------------------- Lists : '+ str(foundWord))
    print('found ' +str(match) + ' out of ' + str(len(dataArray)))


    timeNeeded = datetime.now() - start_time
    print('Time needed: '+ str(timeNeeded))

  #  global total_time
    total_time+=timeNeeded.total_seconds()
    print('Time total: ' + str(total_time) + ' Sec')


if __name__ == '__main__':

    imageNames= os.listdir(dir_path)
    noOfImages=len(imageNames)
    print('no of images: '+ str(noOfImages))
    for imageName in imageNames:
        dbName = imageName.split('.')
        run_vision(imageName,dbName[0])
    #run_vision('img491.jpg')

    print('\n\n\n *************** Analysis Details: all together *************')
    print('\n Number of Image: '+ str(len(imageNames)))
    print('\n Total Word in DB: ' + str(totalWordsinDB))
    print('\n Total Word Found: ' + str(totalMatch))
    print('\n Success Rate: ' + str(totalMatch*100/totalWordsinDB)+ ' %')

    print('\n Total Time needed to analysis ' + str(len(imageNames)) + ' images: ' + str(total_time)+ ' seconds, \n  Average: '+str(total_time/len(imageNames)) + ' Sec/image')
    print ('\n No Text Found Image list '+ str(notFoundList))
