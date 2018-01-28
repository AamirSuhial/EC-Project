# AWS Java Application
Implements AWS java SDK in form of a Spring Boot Application. API that help you to use the AWS rekognition to lable detection.
User can use multiple images as image list in photoname.

## Getting Started
Clone the repository over you local machine or put it over cloud EC2 instance. Add host the on your EC2 instance for better perfromance.

## Prerequisites
Need User's machine to be installed and configured with AWS CLI and configured with user profile to use AWS features.
Refer AWS CLI installation and configration notes.

### JSON model
As JSON request Model is:
{
	"photoname": ["Image1.jpg", "2.jpg", "Image2.jpg"],
	"bucketName": "S3BucketName"
}
### Add UserProfile name.
On ECAssignmentApplication.java User user profile name configured using CLI profile configuration instructions of AWS.
## Authors
Prateek Narula - Initial work

## License
Needs no License
