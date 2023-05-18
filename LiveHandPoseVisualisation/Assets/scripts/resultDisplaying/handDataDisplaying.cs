/*
        _
    .__(.)<  (KWAK)
     \___)    
~~~~~~~~~~~~~~~~~~~~
*/

using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Globalization;
using UnityEngine;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;


public class handDataDisplaying : MonoBehaviour
{
    /*
     Receive pose data from a TCP client and displays it on an OVR hand (can be real or estimated motion capture from a model)
     This class is an adaption from Martin Colot Master thesis 2022 and from https://github.com/ConorZAM/Python-Unity-Socket
    */

    public Transform[] reconstructedHand;
    
    Thread thread;
    public int connectionPort = 25001;
    TcpListener server;
    TcpClient client;
    bool running;
    string currentPoseString;

    private int degreesOfFreedom = 17;

    private List<List<Quaternion>> lastRotations = new List<List<Quaternion>>();
    public int smooth = 1;


    private void Start()
    {
        // endRotationIndex = startRotationIndex + 17;

        // Receive on a separate thread so Unity doesn't freeze waiting for data
        ThreadStart ts = new ThreadStart(receiveData);
        thread = new Thread(ts);
        thread.Start();
    }

    private void receiveData() {

        /*  Thread receiving the data from the TCP client and updating the variable dataReceived 
            Adapted from https://github.com/ConorZAM/Python-Unity-Socket
        */

        // Create the server
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();

        // Create a client to get the data stream
        client = server.AcceptTcpClient();

        // Start listening
        running = true;
        while (running) {
            
            // Read data bytes from the network stream
            NetworkStream nwStream = client.GetStream();
            byte[] buffer = new byte[client.ReceiveBufferSize];
            int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

            // Decode the bytes into a string
            string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);
            
            // If we received some data
            if (dataReceived != null && dataReceived != "") {
                
                // Update the currentPoseString variable that will be used by the FixedUpdate method
                currentPoseString = dataReceived;
            } else {
                // Connection broken by the Python client
                running = false;
            }
        }
        // Stop the C# server and client gracefully
        server.Stop();
        client.GetStream().Close();
        client.Close();
    }


    void FixedUpdate() {

        /*  The Update method is called once per frame 
            Adapted from Martin Colot Master thesis 2022
        */

        // Get the latest pose string received by the TCP thread
        string poseString = currentPoseString;

        if (poseString != null && poseString != "") {

            List<Quaternion> boneRotations = new List<Quaternion>();

            // Split on each joint and create a Quaternion from their Euler coordinates
            string[] jointStringArray = poseString.Split(new[] { ';' }, StringSplitOptions.RemoveEmptyEntries);

            for(int i=0; i < degreesOfFreedom; ++i) {
                boneRotations.Add(Quaternion.Euler(stringToVector3(jointStringArray[i])));
            }

            lastRotations.Add(boneRotations);
            while (lastRotations.Count > smooth)
            {
                lastRotations.RemoveAt(0);
            }

            for (int i = 0; i < reconstructedHand.Length; ++i)
            {
                Quaternion mean = new Quaternion(0, 0, 0, 0);
                for (int j = 0; j < lastRotations.Count; ++j)
                {
                    Quaternion q = lastRotations[j][i];
                    int c = lastRotations.Count;
                    mean = new Quaternion(mean.x + q.x / c, mean.y + q.y / c, mean.z + q.z / c, mean.w + q.w / c);
                }
                reconstructedHand[i].localRotation = mean;
            }

        }
    }


    private Vector3 stringToVector3(string jointString)
    {
        // Split the joint string into a string vector of its Euler coordinates 
        string[] coordinates = jointString.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries);
        
        // Return the coordinates as a Vector3 object
        return new Vector3(float.Parse(coordinates[0], CultureInfo.InvariantCulture.NumberFormat), 
                           float.Parse(coordinates[1], CultureInfo.InvariantCulture.NumberFormat), 
                           float.Parse(coordinates[2], CultureInfo.InvariantCulture.NumberFormat));;

    }
}
