import boto3
from datetime import datetime
import io
import os

imageTitle='airplane'
#imageTitle='ant'
#imageTitle='barrel'

BUCKET = "dataset-"+imageTitle


#aws rekognition detect-labels --image '{"S3Object":{"Bucket":"ishaon","Name":"shaon.JPG"}}'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()

def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""

    keys = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


def detect_labels(bucket, key, max_labels=10, min_confidence=90):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		#MaxLabels=max_labels,
		#MinConfidence=min_confidence,
	)
    return response['Labels']


def run_rekognition(key):
    start_time = datetime.now()
    global total_time
    global success


    print('\n\n*********** Analysis ' + key + ' *************')
    print('\nLabels:\n')
    found = 0
    for label in detect_labels(BUCKET, key):
        print "{Name} - {Confidence}%".format(**label)
        if(label['Name'].upper() == imageTitle.upper()):
            success += 1
            found = 1

    print('\n Result: ')
    if(found == 0):
        print('\n Not Found ' + imageTitle + ' in ' + key)
        notFoundList.append(key)
    else:
        print('\n Match Found')

    timeNeeded = datetime.now() - start_time
    print('\n Time needed: '+ str(timeNeeded))

  #  global total_time
    total_time+=timeNeeded.total_seconds()
    print('\n Time total: ' + str(total_time) + ' Sec')



if __name__ == '__main__':
    s3 = boto3.client('s3')

    keyList = get_s3_keys(BUCKET)
    print('keylist ' +str(keyList))
    noOfImages = len(keyList)

    for key in keyList:
        run_rekognition(key)

    print('\n\n\n *************** Analysis Details: '+imageTitle+' *************')
    print('\n Number of Image: '+ str(len(keyList)))
    print ('\n Found '+ imageTitle + ' in image: ' + str(success) + ' times')
    print(' success rate: ' + str(success * 100 / noOfImages) + '%')
    print('\n Total Time needed to analysis ' + str(len(keyList)) + ' images: ' + str(total_time)+ ' seconds, \n  Average: '+str(total_time/len(keyList)) + ' Sec/image')
    print ('\n Not Found Image list '+ str(notFoundList))