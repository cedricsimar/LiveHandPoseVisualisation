# LiveHandPoseVisualisation
Stream hand poses from Python and visualise them live in Unity
This application will help us to visualise in real-time poses estimated by our AI model from EMG activity (mainly for demonstration purposes).

The Python streamer allows to stream on a TCP socket at at specific frequency, and without drifts, strings or ndarrays of an Oculus hand pose.
The Unity application enables the visualisation of the received hand pose in real-time.

<img align="left" width="400" height="350" 
     src="https://drive.google.com/uc?export=view&id=1q9HsWYOo2QHuH8OHAyerCYtwBhIS9nn8"
     alt="image"
     style="display: block; margin-right: auto; margin-left: auto; width: 90%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)" />


# Notes
Stream poses to address 127.0.0.1 on port 25001 to move the hand representing the true pose (left) and to address 127.0.0.1 on port 25002 to move the hand representing the AI estimated pose from EMG  (right)

The main files where the streaming magic happens are:
  - LiveHandPoseVisualisation/HandPoseStreamer/pose_streamer.py
  - LiveHandPoseVisualisation/LiveHandPoseVisualisation/Assets/scripts/resultDisplaying/handDataDisplaying.cs

# Dependencies
  - Streamer: Python 3.10 with Numpy (+ MNE for working example 2)
  - Visualisation: Unity 2020.3.16f1

# Credits
The code of this work was based on/adapted from:
  - Martin Colot Master thesis code in Unity for hand visualisation
  - https://github.com/ConorZAM/Python-Unity-Socket for the TCP socket connection

```
    .__(.)<  (KWAK)
     \___)    
~~~~~~~~~~~~~~~~~~~~
```
