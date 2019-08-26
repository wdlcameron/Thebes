Note: Thebes has been restructured and this readme needs to be redone!

# Thebes
An approach to automatically segment fluorescence images as well as to extract and organize useful readouts beyond intensity

## Acknowledgements:
Network training is being developed from a fork of Lightnet
<p align = "center">
  <a href="https://eavise.gitlab.io/lightnet/">
<img src="https://eavise.gitlab.io/lightnet/_static/lightnet.svg" alt "Lightnet Logo" width="144" height="144"> 
  </a>
</p>


## Table of Contents
- [Overview](#overview)
- [Warnings](#warnings)
- [Core Features](#core-features)
- [Quick Start](#quick-start)
- [Status](#status)


## Core Features
- Automated ROI selection for quick analysis of fluroescence images
- Automatic organization of output data into logical structures
- Advanced configuration through as single external text file so that multiple users can safely use the plugin across multiple experiements
- Automatic alignment of ROIs to follow single cell behaviour across multiple time or treatment points
- Debug mode to provide a visualization of the analysis so that you can ensure that it is working correctly 


For the training folder:
- Simple box creation in imageJ
- Automatic creation of PASCAL-VOC labels from imageJ selections that are ready to be used for training
- Preparation of the labels for training using a slightly modified training script from the lightnet module.



## Quick Start
The machine learning aspect of the main program requires that you have already trained weights for the lightnet implementation of YOLOV2.  If this is not the case, you can train a new network using the files in YOLO network training.  Documentation for these plugins will also be found there at a later date.  Alternatively, set machine_learning_mode to false and you will have an algorithmic solution to image segmentation, although the segmentations are more conservative.

Cell masking and segementation weights were trained using a modified version of the Fast.AI Dynamic U-Net.  Please see the Segmentation Model Trainer repository in order to train your own weights (or for access to pretrained weights)

For the main program, set debug_mode to True in order to see useful outputs as you learn how to use the program.  
To run the main program, open the Thebes Analysis Suite Jupyter notebook and follow the instructions.   

### The config.txt file
The config.txt file will contain all of the important parameters for your experiment.  Most of the parameters will not change experiment to experiment, but it is important to make sure that they are set up properly for your particular setup. In particular, check that the following are correct for you:
- suffix: the suffix for your data files.  If it is an ome file, be sure to include that part of it (ex. ome.tif)
- root_dir_same_treatment: set to true if you want the results from multiple folders to be pooled together.  Alternatively, set to false if you want each folder to be treated as a different image set
- image_type_array: The plugin will currently only process images of the types "Anisotropy" and "Intensity", but this may change in the future.  If you are processing Anisotropy images, make sure you also set the corresponsing Anisotropy Attrubutes in the config file


## Advanced Configuration
Advanced configuration will be handled through the config.txt file.  Documentation will become available as the project develops.

