# Kinect live processing for industrial safety applications &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/SebastianPartarrieu/live-kinect/blob/master/LICENSE)
To help the industrial adoption of low-cost sensors for safety applications, this repository provides a proof-of-concept of person segmentation with depth estimation and point cloud rendering using the Kinect v2 sensor.

The Kinect v2 provides RGB + IR information: we use the RGB to perform live person segmentation using either (i) the best performing models available on hugging face to benchmark or (ii) openvino lightweight implementations that can run on an intel CPU. Once the segmentation masks are acquired we can use these to extract the humans from the Kinect depth maps and then estimate the distance of each human to the sensor. Finally, after the depth estimation, we can render 3D point clouds of each visible human. This workflow could then be fed downstream to a navigating robot using the input data to update its trajectory.

> Disclaimer: There are both experimental and more mature scripts within the repository.

## Installation

### Getting started

Depending on what your use case is, there are different installation options available.
System specifications:
Install [openvino_notebooks](https://github.com/openvinotoolkit/openvino_notebooks/wiki/Conda#step-4-install-the-packages) by following the linked instructions. It will be easier to follow the rest if you create a conda environment as explained and install the correct packages using requirement_openvino.txt file.

If you intend to process the Kinectv2 data flow, you will need to install specific libraries (CAREFUL, the installation guide provided below works only with Linux):
- libfreenect2 : follow the instructions here : https://github.com/OpenKinect/libfreenect2
- freenect2-python : python wrapper for libfreenect2, allows a more pythonic way of processing the kinect v2 frames. See https://rjw57.github.io/freenect2-python/.
> Careful: for the freenect2-python installation, you don't need to reinstall libfreenect2, you just need to activate your favorite conda environment, set the system environment variable and then install the python wrapper.
```
conda activate your_openvino_convda_env
export PKG_CONFIG_PATH=$HOME/freenect2/lib/pkgconfig
pip install --user freenect2
```
You will probably still run into some issues even after following these installation guides when trying to run ```kinect_real_time.py``` or other scripts using libfreenect2. It seems there are some path issues that were [fixed](https://github.com/rjw57/freenect2-python/issues/6) by creating a symbolic link like so:
```
sudo ln -s $HOME/freenect2/lib/libfreenect2.so.0.2 /usr/lib/libfreenect2.so.0.2
```

### Repository structure
```
.
├── docs
├── models
|   ├── model-segmentation
|      ├── instance-segmentation-person-0007
|          ├── FP16
|             ├── instance-segmentation-person-0007.bin
|             └── instance-segmentation-person-0007.xml
|          └── FP32
|             ├── instance-segmentation-person-0007.bin
|             └── instance-segmentation-person-0007.xml
├── code
```

## Developing

### Built with


### Prerequisites
If anything extra is needed to set up the dev environment.


### Configuration
What to change and where to change it.

## Authors
Emma Bou Hanna & Sebastian Partarrieu
