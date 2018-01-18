/*
 * Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
**/

var express = require('express'),
    app= express(),
    http= require("http").Server(app).listen(8080),
    upload = require('express-fileupload');

// Load the SDK and UUID
var AWS = require('aws-sdk');
var uuid = require('node-uuid');

AWS.config.update({

    region:"us-east-1"});

app.use(upload());

console.log('Server started at 8080');

app.get('/', function(req,res){
    res.sendFile(__dirname+"/index.html");

});


app.post('/', function(req,res){
    if(req.files){
        var file = req.files.pic,
            filename = file.name;
        console.log(file.name);

        //aws s3

        var bucket = new AWS.S3({params: {Bucket: 'ishaon'}});
        var params = {Key: filename.toString(), ContentType: file.type, Body: file.data};
        bucket.upload(params, function (err, data) {
            if(err){
                console.log("aws err: "+ err);
            }
            else{
                console.log("s3 uploaded successfully")
                imageAnalysisByAws(filename.toString(),function(returnValue){
                    awsResult=returnValue;
                    gcloud();

                });
            }

        });


        /*
        s3.abortMultipartUpload(params, function (err, data) {
            if (err) console.log(err, err.stack); // an error occurred
            else     console.log(data);           // successful response
        });
*/

        //amazon end
        function gcloud() {

            file.mv('./uploads/' + filename, function (err) {
                if (err) {
                    console.log(err);
                    res.send('error occurs: ' + err);
                } else {

                    imageAnalysis(filename, function (returnValue) {
                        res.send(awsResult+" :" +returnValue);
                    });

                    //res.send(data);
                }

            })
        }



    }
});



/*// Create an S3 client
var s3 = new AWS.S3();

// Create a bucket and upload something into it
var bucketName = 'node-sdk-sample-' + uuid.v4();
var keyName = 'hello_world.txt';

s3.createBucket({Bucket: bucketName}, function() {
  var params = {Bucket: bucketName, Key: keyName, Body: 'Hello World!'};
  s3.putObject(params, function(err, data) {
    if (err)
      console.log('bucket error: '+ err)
    else
      console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
  });
});*/



const vision = require('@google-cloud/vision');

// gcloud vision analysis
function imageAnalysis(thisImage, callback) {
    console.log("gcloud vision analysis")
    const client = new vision.ImageAnnotatorClient();
    var labelArray = new Array();
// Performs label detection on the image file
    client
        .labelDetection("./uploads/"+thisImage)
        .then(results => {
        const labels = results[0].labelAnnotations; //cropHintAnnotation


    console.log('Labels:');
    //labels.forEach(label => console.log(label.description));

    labels.forEach(label => labelArray.push(label.description));
    console.log('thevalue: '+labelArray.toString());
    callback('<h4>GCloud Analysis: </h4>'+labelArray.toString());
    //return labelArray.toString();

})
.catch(err => {
        console.error('ERROR:', err);
});


}

/*
npm install --save @google-cloud/vision
npm install express-fileupload

to upload to google cloud the code
gcloud app deploy
gcloud app browse
 */

function imageAnalysisByAws(imageName, callback){
    console.log("aws analysis");
    var paramDetectLabels={

        "Image": {
            "S3Object": {
                "Bucket": "ishaon",
                "Name": imageName,

            }
        }
    }
    var rekognition = new AWS.Rekognition();

//aws rekognition detect-labels --image '{"S3Object":{"Bucket":"ishaon","Name":"shaon.JPG"}}'
    rekognition.detectLabels(paramDetectLabels, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else {
            // console.log(data);           // successful response
            console.log(data.Labels);
            var rlabel="<h4>AWS Analysis: </h4>" + JSON.stringify(data.Labels) + "<br /><br />";
            callback (rlabel);

        }
    });

}
