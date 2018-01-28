# AWS Java Application
Implements AWS java SDK in form of a Spring Boot Application API that help to use the AWS rekognition for label detection.
User can use multiple images as image list in photoname.

## Getting Started
Clone the repository over you local machine or put it over cloud EC2 instance. Host the application on EC2 instance for better perfromance.

## Prerequisites
Needs User's machine to be installed and configured with AWS CLI and configured with user profile to use AWS features.
Refer AWS CLI installation and configration notes.

### JSON model
As JSON request Model is:
{
	"photoname": ["Image1.jpg", "2.jpg", "Image2.jpg"],
	"bucketName": "S3BucketName"
}
### API method
You need to use '/detectlabel' method in front of your hosted API URI to access the method. 

### Add UserProfile name.
On ECAssignmentApplication.java use userprofile name configured using CLI profile configuration instructions of AWS.
## Authors
Prateek Narula - Initial work

## License
Needs no License
