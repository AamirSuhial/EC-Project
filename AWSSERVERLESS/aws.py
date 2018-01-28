from __future__ import print_function

import boto3
from decimal import Decimal


def detect_labels(bucket, key, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
    )
    return response['Labels']

def lambda_handler(event, context):
    arrayOFLabels = []
    BUCKET = event['bucket']
    KEY = event['key']

    for res in detect_labels(BUCKET,KEY):
        name = res["Name"]
        confi = res["Confidence"]
        arrayOFLabels.append(name)
        arrayOFLabels.append(confi)
    return arrayOFLabels


#######DECTECT FACES##########

from __future__ import print_function
import boto3
from decimal import Decimal
import json
import urllib

FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")

#detect faces in aws
def detect_faces(bucket, key, attributes=['ALL'], region="us-east-1"):
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
    
def lambda_handler(event, context):
    responsee = []
    BUCKET = event['bucket']
    KEY = event['key']
    
    for face in detect_faces(BUCKET, KEY):
        responsee.append("Face ({Confidence}%)".format(**face))
    # emotions
        for emotion in face['Emotions']:
            responsee.append("  {Type} : {Confidence}%".format(**emotion))
    return responsee


##index of faces

from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

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

def lambda_handler(event, context):
    responses = []
    BUCKET = event['bucket']
    KEY = event['key']
    COLLECTION = "BLUEPRINT_COLLECTION"
    IMAGE_ID = event['image_id']
    for record in index_faces(BUCKET, KEY, COLLECTION, IMAGE_ID):
    face = record['Face']
    responses.append("Face ({}%)".format(face['Confidence']))
    responses.append("  FaceId: {}".format(face['FaceId']))
    responses.append("  ImageId: {}".format(face['ImageId']))
    return responses

##compare faces

from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

def compare_faces(bucket, key, bucket_target, key_target, region="us-east-1"):
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
    )
    responses = []
    responses.append(response['SourceImageFace'])
    responses.append(response['FaceMatches'])
    return responses
    
def lambda_handler(event, context):
    resposee = []
    BUCKET = event['bucket']
    KEY = event['key']
    COLLECTION = "BLUEPRINT_COLLECTION"
    imagetobecomparedwith = event['targetImage']
    
    matches = compare_faces(BUCKET, KEY, BUCKET,imagetobecomparedwith)
    resposee.append("Source Face ({Confidence}%)".format(**matches[0]))
    for match in matches[1]:
        resposee.append("Target Face ({Confidence}%)".format(**match['Face'])) 
        resposee.append("  Similarity : {}%".format(match['Similarity']))
    return resposee

    ##faces in an Image
    from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

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

def lambda_handler(event, context):
    responses = []
    BUCKET = event['bucket']
    KEY = event['key']
    COLLECTION = "BLUEPRINT_COLLECTION"

    for record in search_faces_by_image(BUCKET, KEY, COLLECTION):
        face = record['Face']
        responses.append("Matched Face ({}%)".format(record['Similarity']))
        responses.append("  FaceId : {}".format(face['FaceId']))
        responses.append("  ImageId : {}".format(face['ExternalImageId']))
    return responses