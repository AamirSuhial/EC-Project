package com.assignment.ecassignment;

import com.assignment.models.DetectLabel;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.services.rekognition.model.*;

import java.util.List;

@SpringBootApplication
@RestController
public class EcassignmentApplication {

	public static void main(String[] args) {
		SpringApplication.run(EcassignmentApplication.class, args);
	}


	@RequestMapping(method = RequestMethod.POST, value="/detectlabel")
	public ResponseEntity<?> detectlable (@RequestBody DetectLabel detectLabel) {
		List<String> photolist = detectLabel.getPhotoname();
		String bucket = detectLabel.getBucketName();

		AWSCredentials credentials;
		try {
			credentials = new ProfileCredentialsProvider("PrateekNarula").getCredentials();
		} catch (Exception e) {
			throw new AmazonClientException("Cannot load the credentials from the credential profiles file. "
					+ "Please make sure that your credentials file is at the correct "
					+ "location (/Users/userid/.aws/credentials), and is in a valid format.", e);
		}

		AmazonRekognition rekognitionClient = AmazonRekognitionClientBuilder
				.standard()
				.withRegion(Regions.EU_WEST_1)
				.withCredentials(new AWSStaticCredentialsProvider(credentials))
				.build();
		List<Label> labels = null;
		for (String photo:photolist ) {


			DetectLabelsRequest request = new DetectLabelsRequest()
					.withImage(new Image()
							.withS3Object(new S3Object()
									.withName(photo).withBucket(bucket)))
					.withMaxLabels(10)
					.withMinConfidence(75F);
			try {
				DetectLabelsResult result = rekognitionClient.detectLabels(request);
				labels = result.getLabels();
			} catch (AmazonRekognitionException e) {
				e.printStackTrace();
			}
		}
		if(labels.size()>0) {
			return ResponseEntity.status(HttpStatus.FOUND).body(labels);
		}
		else {
			return ResponseEntity.status(HttpStatus.NO_CONTENT).body("No Labels detected");
		}

	}
}
