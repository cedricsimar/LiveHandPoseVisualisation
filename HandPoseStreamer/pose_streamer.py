"""
        _
    .__(.)<  (KWAK)
     \___)    
~~~~~~~~~~~~~~~~~~~~
"""

import socket
import time
import threading
import numpy as np


class Pose_Streamer:

    BUFER_SIZE = 2048   # bytes (max size of a pose string is 1037 bytes)
    
    def __init__(self, sfreq, host, port):
        """
        sfreq: sending frequency (number of data per second sent on the socket)
        host: host address
        port: connection port
        """

        self.host = host
        self.port = port
        self.sending_interval = 1/sfreq  # time between each send command on the socket
        
        self.connected = False
        self.streaming = False
        self.information_sent = False

        self.buffer = ""

        # Define a TCP socket (SOCK_STREAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Create the streaming thread variable with the target method
        self.streaming_thread = threading.Thread(target=self._streaming_thread)


    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Connection successful on host " + self.host + ":" + str(self.port))
            self.connected = True
        except Exception as e:
            print(e)
            print("Cannot connect the socket on host " + self.host + ":" + str(self.port))
    
    
    def disconnect(self):
        self.socket.close()
        self.connected = False
        print("Connection closed with host " + self.host + ":" + str(self.port))
        

    def send(self, data):
        if not isinstance(data, str):
            raise TypeError("Data should be of type str")

        try:
            self.socket.sendall(data.encode("utf-8"))
        except Exception as e:
            print(e)
            print("Cannot send the encoded data through socket on host " + self.host + ":" + str(self.port))       


    def receive(self):
        try:
            received_data = self.socket.recv(self.BUFER_SIZE).decode("utf-8")
        except Exception as e:
            print(e)
            print("Cannot receive data through socket on host " + self.host + ":" + str(self.port))
        
        return received_data
    

    def start_streaming(self):
        
        # Connect to the server
        self.connect()
    
        # Start the streaming thread
        self.streaming = True
        print("Data streaming started")
        self.streaming_thread.start()
               

    def _streaming_thread(self):

        # Use time() and sleep to avoid interval drift while streaming
        start_time = time.time()
        while self.connected and self.streaming:
            self.send(self.buffer)
            self.information_sent = True
            time.sleep(self.sending_interval - ((time.time() - start_time) % self.sending_interval))


    def stop_streaming(self):
        
        self.streaming = False
        self.streaming_thread.join()
        print("Data streaming stopped")
        self.disconnect()
        

    def send_pose(self, pose):
        self.information_sent = False

        if isinstance(pose, str):
            # Place the pose into the buffer
            self.buffer = pose

        elif isinstance(pose, np.ndarray):
            # Convert the pose array to str and place it into the buffer
            pose = np.char.mod('%f', pose) # precision (e-6) is acceptable since it represents degrees
            pose = ';'.join([','.join(x) for x in [pose[i:i+3] for i in range(0, len(pose), 3)]]) + ';' 
            self.buffer = pose
        
        else:
            raise TypeError("The pose object should be of type str or ndarray")

