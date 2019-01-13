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


## Overview
This is an attempt to simplify the process of training, testing and creating training sets for the lightnet architecture.  It is currently based on a combination of imageJ/Fiji (which is familiar to most in the microscopy community) and Python.

Future implementation may also modify core aspects of the Lightnet architecture (ex. updated it to YOLO3, etc.)

## Warnings
This program is still in early development and still needs to be optimized for a broader audience.  Please let me know if there are any issues that pop up (or instructions are unclear) and I will do my best to address them!


## Core Features
- Automated ROI selection for quick analysis of fluroescence images
- Automatic organization of output data into logical structures
- Advanced configuration through as single external text file so that multiple users can safely use the plugin across multiple experiements
- Automatic alignment of ROIs to follow single cell behaviour across multiple time or treatment points
- Debug mode to provide a visualization of the analysis so that you can ensure that it is working correctly 
- (In Progress) Incorporation of machine learning to generate precise segmentations of cells, providing additional information


For the training folder:
- Simple box creation in imageJ
- Automatic creation of PASCAL-VOC labels from imageJ selections that are ready to be used for training
- Preparation of the labels for training using a slightly modified training script from the lightnet module.



## Quick Start
The machine learning aspect of the main program requires that you have already trained weights for the lightnet implementation of YOLOV2.  If this is not the case, you can train a new network using the files in YOLO network training.  Documentation for these plugins will also be found there at a later date.  Alternatively, set machine_learning_mode to false and you will have an algorithmic solution to image segmentation, although the segmentations are more conservative.

For the main program, set debug_mode to True in order to see useful outputs as you learn how to use the program.  
To run the main program, open the Jupyter notebook Anisotropy and navigate to the cell that says "Start Here".  In the next cell, modify the paths to your config.txt file and the path to your data.  The program will load the parameters from your config.txt file and store them in the Parameters instance of the ImagingParameters class.  This will be the main class for your experiment and will hold references to all of the experimental variables as well as the final panda dataframes. Running the next cell will analyze your images for you and store panda dataframes containing your organized data.  The cells after that contain a module to output your data to excel as well as some organizational tools, but they are still works in progress.

### The config.txt file
The config.txt file will contain all of the important parameters for your experiment.  Most of the parameters will not change experiment to experiment, but it is important to make sure that they are set up properly for your particular setup. In particular, check that the following are correct for you:
- suffix: the suffix for your data files.  If it is an ome file, be sure to include that part of it (ex. ome.tif)
- root_dir_same_treatment: set to true if you want the results from multiple folders to be pooled together.  Alternatively, set to false if you want the 
- machine_learning_mode: set to false if you want to play around with the program without training the weights.  If set to true, make sure you also have the network settings set correctly
- image_type_array: The plugin will currently only process images of the types "Anisotropy" and "Intensity", but this may change in the future.  If you are processing Anisotropy images, make sure you also set the corresponsing Anisotropy Attrubutes in the config file

## Advanced Configuration
Advanced configuration will be handled through the config.txt file.  Documentation will become available as the project develops.


## Status
Early stage of development.  The first iteration of the pipeline is complete but it is not user friendly.  As the project develops, the jupyter notebook segmented into individual python scripts and will be replaced by a demo notebook to teach users how to use it.  A GUI is also in the works.  
