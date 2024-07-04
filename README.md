# Spam Detector
**Author**: Colton .S.T.T Fridgen
## Overview
Spam detector is a Google cloud app that uses Gmail API and a Multinomial Naive Bayes classification model to move unread spam emails into the users spam folder
### spam_detection_model.py
collects test data and trains the Multinomial Naive Bayes (MNB) Classification model
### spam_detector.py
contains **load_model()** function for loading the MNB classification model and **predict()** function for predicting a message as spam or not
### spam_detector_app.py
this file uses **spam_detector.py** and the google client library to scan unread emails for spam and placing them in the spam folder