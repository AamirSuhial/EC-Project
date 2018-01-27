import boto3
from datetime import datetime
import io
import os

imageTitle='s1'
#imageTitle='ant'
#imageTitle='barrel'

BUCKET = "dataset-face-s1"


#aws rekognition detect-labels --image '{"S3Object":{"Bucket":"ishaon","Name":"shaon.JPG"}}'

total_time=0.00
noOfImages=0
success = 0
notFoundList = list()
noOfTotalFace = 0

def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""

    keys = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")

def detect_faces(bucket, key, attributes=['ALL']):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_faces(
	    Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
	    Attributes=attributes,
	)
    return response['FaceDetails']


def run_rekognition(key):
    start_time = datetime.now()
    global total_time
    global success

    faces = detect_faces(BUCKET, key)
    print('\n\n*********** Analysis ' + key + ' *************')
    print('\nFaces:\n')
    print('Number of Face found: ' + str(len(faces)))
    global noOfTotalFace
    noOfTotalFace = noOfTotalFace + len(faces)

    print('\n Result: ')
    if (len(faces) == 0):
        print('\nNo Face Found')
        notFoundList.append(key)
        return


    for face in faces:
        print "Face ({Confidence}%)".format(**face)
        # emotions
        for emotion in face['Emotions']:
            print "  {Type} : {Confidence}%".format(**emotion)
        # quality
        '''for quality, value in face['Quality'].iteritems():
            print "  {quality} : {value}".format(quality=quality, value=value)
        # facial features
        for feature, data in face.iteritems():
            if feature not in FEATURES_BLACKLIST:
                print "  {feature}({data[Value]}) : {data[Confidence]}%".format(feature=feature, data=data)'''



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
        run_rekognition(key)

    print('\n\n\n *************** Analysis Details:  *************')
    print('\n Number of Image: ' + str(len(keyList)))
    print ('\n No of Face found: ' + str(noOfTotalFace) + ' times')
    # case s1 face per image
    print('success rate: ' + str(noOfTotalFace * 100 / (20 * 20)) + '%')
    #case s2 face per image
    #print('success rate: ' + str(noOfTotalFace * 100 / noOfImages) + '%')
    print('\n Total Time needed to analysis ' + str(len(keyList)) + ' images: ' + str(total_time) + ' seconds, \n  Average: ' + str(total_time / len(keyList)) + ' Sec/image')
    print ('\n Not Found Image list ' + str(notFoundList))