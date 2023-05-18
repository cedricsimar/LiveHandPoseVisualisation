"""
        _
    .__(.)<  (KWAK)
     \___)    
~~~~~~~~~~~~~~~~~~~~
"""

import time
import sys
sys.path.append("../")
from HandPoseStreamer.pose_streamer import Pose_Streamer

def working_example_1(): 

    # Working example of a TCP stream of pose data from Python to Unity 
    # One pose is made of 17 triplets of coordonates, each ending with the ';' delimiter

    # Working example 1 implement a stream of pose data from a csv file at 60Hz

    degrees_of_freedom = 17

    with open("./hand_data.csv") as f:
        data = [line.strip() for line in f.readlines()]
    
    # Split the lines between the true and estimated poses
    true_data = [';'.join(line.split(';')[:degrees_of_freedom]) for line in data]
    true_data = [k + ';' for k in true_data]  # add the ; delimiter at the end of the pose
    est_data = [';'.join(line.split(';')[degrees_of_freedom:]) for line in data] # ; already there

    sfreq = 60 # since poses in the data file are recorded at 60Hz
    sending_interval = 1/sfreq
    ps_true = Pose_Streamer(sfreq, "127.0.0.1", 25001)
    ps_est = Pose_Streamer(sfreq, "127.0.0.1", 25002)
    ps_true.start_streaming()
    ps_est.start_streaming()
    i = 0

    start_time = time.time()
    while True:
        try:
            i %= len(data)        
            ps_true.send_pose(true_data[i])
            ps_est.send_pose(est_data[i])
            i += 1
            time.sleep(sending_interval - ((time.time() - start_time) % sending_interval))

        except KeyboardInterrupt:
            ps_true.stop_streaming()
            ps_est.stop_streaming()
            break


if __name__ == "__main__":
    working_example_1()