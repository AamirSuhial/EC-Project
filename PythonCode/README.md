## AWS Rekognition Vs. Google Cloud Vision
## Run Python Code from Local PC installing AWS and Google Cloud SDK

###Google Cloud Vision Benchmark

### install gcloud => https://cloud.google.com/storage/docs/gsutil_install
create a project from console
then initialize your credential with
gcloud init

now run any pythoncode with GCV.....py (GCV stands for GoogleCloudVision)
python GCVLabelDetection.py
or
python GCVFaceDetection.py

There is an output-google.text contains some result.

###AWS Rekognition setup

install AWS SDK through
pip install boto3
aws configure
(setup your access and secret key)

to use my S3 set your region as us-east-1

run python AWSAWSFaceDetection.py

output-aws.txt contains some result


