from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

BUCKET = "imagebucketrecognition"
KEY = ["1.jpg","6.jpg"]
COLLECTION = "my-collection-id"
IMAGE_ID = KEY  # S3 key as ImageId

# Note: you have to create the collection first!
# rekognition.create_collection(CollectionId=COLLECTION)

###indexfaces on aws

def index_faces(bucket, key, collection_id, image_id=None, attributes=(), region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.index_faces(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		ExternalImageId=image_id,
	    DetectionAttributes=attributes,
	)
	return response['FaceRecords']


for record in index_faces(BUCKET, KEY, COLLECTION, IMAGE_ID):
	face = record['Face']
	# details = record['FaceDetail']
	print "Face ({}%)".format(face['Confidence'])
	print "  FaceId: {}".format(face['FaceId'])
	print "  ImageId: {}".format(face['ImageId'])


##search faces by image aws
def search_faces_by_image(bucket, key, collection_id, threshold=80, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		FaceMatchThreshold=threshold,
	)
	return response['FaceMatches']

for record in search_faces_by_image(BUCKET, KEY, COLLECTION):
	face = record['Face']
	print "Matched Face ({}%)".format(record['Similarity'])
	print "  FaceId : {}".format(face['FaceId'])
	print "  ImageId : {}".format(face['ExternalImageId'])

# compare faces aws 
def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		TargetImage={
			"S3Object": {
				"Bucket": bucket_target,
				"Name": key_target,
			}
		},
	    SimilarityThreshold=threshold,
	)
	return response['SourceImageFace'], response['FaceMatches']


source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)

# the main source face
print "Source Face ({Confidence}%)".format(**source_face)

# one match for each target face
for match in matches:
	print "Target Face ({Confidence}%)".format(**match['Face'])
	print "  Similarity : {}%".format(match['Similarity'])

# detect labels in aws 
def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']


for label in detect_labels(BUCKET, KEY):
	print "{Name} - {Confidence}%".format(**label)

FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")

#detect faces in aws
def detect_faces(bucket, key, attributes=['ALL'], region="eu-west-1"):
	rekognition = boto3.client("rekognition", region)
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

for face in detect_faces(BUCKET, KEY):
	print "Face ({Confidence}%)".format(**face)
	# emotions
	for emotion in face['Emotions']:
		print "  {Type} : {Confidence}%".format(**emotion)
	# quality
	for quality, value in face['Quality'].iteritems():
		print "  {quality} : {value}".format(quality=quality, value=value)
	# facial features
	for feature, data in face.iteritems():
		if feature not in FEATURES_BLACKLIST:
			print "  {feature}({data[Value]}) : {data[Confidence]}%".format(feature=feature, data=data)

# All functions are evoked by an api call on aws, by event and context. when we call the endpoint it evokes lamda as
def lambda_handler(event, context):
    try:
      #eg we are evoking dectlabels
        response = detect_labels(bucket, key)
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e


## In api call we just fetch the data, and use the deployed api in our benchmarks on JMeter or Apache AB testing.