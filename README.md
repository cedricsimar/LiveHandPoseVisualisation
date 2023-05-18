# LiveHandPoseVisualisation
Stream hand poses from Python and visualise them live in Unity
This application will help us to visualise in real-time poses estimated by our AI model from EMG activity (mainly for demonstration purposes).

The Python streamer allows to stream on a TCP socket at at specific frequency, and without drifts, strings or ndarrays of an Oculus hand pose.
The Unity application enables the visualisation of the received hand pose in real-time.

# Notes
Stream poses to address 127.0.0.1 with 25001 to move the left hand (true pose) and address 127.0.0.1 with 25002 to move the right hand (estimated pose from EMG)

The main files where the magic happens are:
  - LiveHandPoseVisualisation/HandPoseStreamer/pose_streamer.py
  - LiveHandPoseVisualisation/LiveHandPoseVisualisation/Assets/scripts/resultDisplaying/handDataDisplaying.cs

# Dependencies
Streamer: Python 3.10 with Numpy (+ MNE for working example 2)
Visualisation: Unity 2020.3.16f1

# Credits
The code of this work was based on/adapted from:
  - Martin Colot Master thesis code in Unity for hand visualisation
  - https://github.com/ConorZAM/Python-Unity-Socket for the TCP socket connection

        _
    .__(.)<  (KWAK)
     \___)    
~~~~~~~~~~~~~~~~~~~~
