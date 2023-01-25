# Kinect live processing for industrial safety applications &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/SebastianPartarrieu/live-kinect/blob/master/LICENSE)
To help the industrial adoption of low-cost sensors for safety applications, this repository provides a proof-of-concept of person segmentation with depth estimation and point cloud rendering using the Kinect v2 sensor.

The Kinect v2 provides RGB + IR information: we use the RGB to perform live person segmentation using either (i) the best performing models available on hugging face to benchmark or (ii) openvino lightweight implementations that can run on an intel CPU. Once the segmentation masks are acquired we can use these to extract the humans from the Kinect depth maps and then estimate the distance of each human to the sensor. Finally, after the depth estimation, we can render 3D point clouds of each visible human. This workflow could then be fed downstream to a navigating robot using the input data to update its trajectory.

> Disclaimer: There are both experimental and more mature scripts within the repository.

## Installation

### Getting started

Depending on what your use case is, there are different installation options available.
System specifications:
Install [openvino_notebooks](https://github.com/openvinotoolkit/openvino_notebooks/wiki/Conda#step-4-install-the-packages) by following the linked instructions.

### Repository structure
```
.
├── docs
├── models
|   ├── model-segmentation
|      ├── instance-segmentation-person-000
|          ├── FP16
|          └── FP32
```

## Developing

### Built with


### Prerequisites
If anything extra is needed to set up the dev environment.


### Configuration
What to change and where to change it.

## Authors
Emma Bou Hanna & Sebastian Partarrieu
