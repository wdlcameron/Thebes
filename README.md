# Bio-Lightnet
Implementation of Lightnet (YOLO in Pytorch) for fluorescence microscopy


## Acknowledgements:
This is being developped from a fork of Lightnet
<p align = "center">
  <a href="https://eavise.gitlab.io/lightnet/">
<img src="https://eavise.gitlab.io/lightnet/_static/lightnet.svg" alt "Lightnet Logo" width="144" height="144"> 
  </a>
</p>


## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Status](#status)


## Overview
This is an attempt to simplify the process of training, testing and creating training sets for the lightnet architecture.  It is currently based on a combination of imageJ/Fiji (which is familiar to most in the microscopy community) and Python.

Future implementation may also modify core aspects of the Lightnet architecture (ex. updated it to YOLO3, etc.)


### Core Features:
- Simple box creation in imageJ
- Automatic creation of PASCAL-VOC labels from imageJ selections that are ready to be used for training


## Quick Start
Run the two imageJ plugins in /YOLO Training Scripts and then run the functions in "YOLO Label Generator.ipynb" to create the pickle file for training.



## Advanced Configuration
Advanced configuration will be handled through the config.txt file.  Documentation will become available as the project develops.


## Status
Early stage of development, but working.  
