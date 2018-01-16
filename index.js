'use strict';
var express = require('express'),
    app= express(),
    http= require("http").Server(app).listen(8080),
    upload = require('express-fileupload');

var AWS = require('aws-sdk');
AWS.config.update({region:"us-east-1"});

app.use(upload());

console.log('Server started at 8080');

app.get('/', function(req,res){
    res.sendFile(__dirname+"/index.html");

});
var awsResult;

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
