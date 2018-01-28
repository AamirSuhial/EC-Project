import boto3
from datetime import datetime
import sys

BUCKET = "text20"
BUCKETDB = "text20database"


total_time=0.00
noOfImages=0
success = 0
notFoundList = list()
noOfTotalText =0
totalWordsinDB = 1
totalMatch = 0

def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""

    keys = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


def detect_text(bucket, key):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_text(
	    Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		}
	)
    return response['TextDetections']


def run_rekognition(key,dbName):
    client = boto3.client("s3")
    result = client.get_object(Bucket=BUCKETDB, Key=str(dbName)+'.txt')
    dataStr = result["Body"].read().decode()
    dataArray = dataStr.split(',')
    global totalWordsinDB
    totalWordsinDB = totalWordsinDB + len(dataArray)

    start_time = datetime.now()
    global total_time

    print('\n*******Analysis: ' + key + '****************\n\n')

    global success
    match = 0
    foundWord = list()

    try:
        texts = detect_text(BUCKET, key)

        print('Number of Text found: ' + str(len(texts)))
        global noOfTotalText
        noOfTotalText = noOfTotalText + len(texts)

        print('\n Result: ')
        if (len(texts) == 0):
            print('\nNo Text Found')
            notFoundList.append(key)
            return

        success = success + 1
        print('Text Detected: ')
        for text in texts:
            print('the text: '+ str(text['DetectedText']))
            for data in dataArray:
                # print('Compare: ' + text.description + ' and ' + data)
                if (text['DetectedText'].upper() == data.upper()):
                    # print('Match found: ' + text.description + ' with ' + data)
                    foundWord.append(text['DetectedText'])
                    match = match + 1
                    global totalMatch
                    totalMatch = totalMatch + 1

    except:
        e = sys.exc_info()[0]
        print('exception throw: '+ str(e))
        notFoundList.append(key)

    print('\n\n --- Analysis for this image')

    print('\nWords in DB: ' + str(len(dataArray)))
    print('Match found: ' + str(match) + ' ----------------------------------------------- Lists : ' + str(foundWord))
    print('found ' + str(match) + ' out of ' + str(len(dataArray)))
    
    timeNeeded = datetime.now() - start_time
    print('\n Time needed: '+ str(timeNeeded))

  #  global total_time
    total_time+=timeNeeded.total_seconds()
    print('\n Time total: ' + str(total_time) + ' Sec')



if __name__ == '__main__':
    s3 = boto3.client('s3')

    keyList = get_s3_keys(BUCKET)
    #print('keylist ' +str(keyList))
    noOfImages = len(keyList)
    print('no of images: ' + str(noOfImages))
    for key in keyList:
        dbName = key.split('.')
        run_rekognition(key,dbName[0])

#    run_rekognition('img2.jpg')


    print('\n\n\n *************** Analysis Details: all together *************')
    print('\n Number of Image: ' + str(len(keyList)))
    print('\n Total Word in DB: ' + str(totalWordsinDB))
    print('\n Total Word Found: ' + str(totalMatch))
    print('\n Success Rate: ' + str(float(totalMatch * 100 / totalWordsinDB)) + ' %')

    print('\n Total Time needed to analysis ' + str(len(keyList)) + ' images: ' + str(
        total_time) + ' seconds, \n  Average: ' + str(total_time / len(keyList)) + ' Sec/image')
    print ('\n No Text Found Image list ' + str(notFoundList))
