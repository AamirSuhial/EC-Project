package com.assignment.models;

import javax.persistence.Entity;
import java.io.Serializable;
import java.util.List;

@Entity
public class DetectLabel implements Serializable {


    List<String> photoname;
    String bucketname;

    public List<String> getPhotoname() {
        return photoname;
    }

    public void setPhotoname(List<String> photoname) {
        this.photoname = photoname;
    }



    public String getBucketName() {
        return bucketname;
    }

    public void setBucketName(String bucketName) {
        bucketname = bucketName;
    }

}
