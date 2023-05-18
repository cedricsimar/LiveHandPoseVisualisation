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

def working_example_2(): 

    # Working example of a TCP stream of pose data from Python to Unity 
    # One pose is made of 17 triplets of coordonates, each ending with the ';' delimiter
    
    # Working example 2 implement a stream of pose data from a MNE fif file from the dataset at 60Hz
    # The sampling frequency of the pose data from the dataset is 2048Hz

    import mne

    sfreq = 512 # used to resample data from 2048Hz to sfreq
    
    data = mne.io.read_raw("./s4_sign1.fif", preload=True).resample(sfreq).get_data("misc")[0:51]
    data = data[:, :sfreq * 60] # 1 minute of data
    
    sending_interval = 1/sfreq
    ps_true = Pose_Streamer(sfreq, "127.0.0.1", 25001)
    ps_est = Pose_Streamer(sfreq, "127.0.0.1", 25002)
    ps_true.start_streaming()
    ps_est.start_streaming()
    i = 0

    start_time = time.time()
    while True:
        try:
            i %= data.shape[1]
            ps_true.send_pose(data[:, i])
            ps_est.send_pose(data[:, i])
            i += 1
            time.sleep(sending_interval - ((time.time() - start_time) % sending_interval))

        except KeyboardInterrupt:
            ps_true.stop_streaming()
            ps_est.stop_streaming()
            break



if __name__ == "__main__":
    working_example_2()
