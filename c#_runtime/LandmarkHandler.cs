using System;
using System.Net;
using System.Net.Sockets;
using HolisticPose;
using Google.Protobuf;
using Microsoft.Azure.Kinect.BodyTracking;

namespace MpAndKinectPoseSender
{
    internal class LandmarkHandler : IDisposable
    {
        UdpClient _sender;
        string _senderUri = "127.0.0.1";
        int _senderPort = 9000;

        UdpClient _receiver;
        string _receiverUri = "127.0.0.1";
        int _receiverPort = 9001;

        readonly Action<SocketException> _socketExceptionCallback;
        readonly Action<ObjectDisposedException> _objectDisposedExceptionCallback;

        HolisticLandmarks _result;

        public LandmarkHandler()
        {
            _sender = new UdpClient();
            var senderEndPoint = new IPEndPoint(IPAddress.Parse(_senderUri), _senderPort);
            _sender.Connect(senderEndPoint);
            _receiver = new UdpClient(_receiverPort);

            _result = new HolisticLandmarks();

            _receiver.BeginReceive(OnReceived, _receiver);
        }

        public void Update(Skeleton skeleton)
        {
            PackResults(skeleton);
        }

        void OnReceived(IAsyncResult result) 
        {
            UdpClient getUdp = (UdpClient)result.AsyncState;
            IPEndPoint ipEnd = null;

            try
            {
                var getByte = getUdp.EndReceive(result, ref ipEnd);
                _result = HolisticLandmarks.Parser.ParseFrom(getByte);
            }
            catch (SocketException e)
            {
                _socketExceptionCallback(e);
                return;
            }
            catch (ObjectDisposedException e) 
            {
                _objectDisposedExceptionCallback(e); 
                return;
            }

            _receiver.BeginReceive(OnReceived, getUdp);
        }

        void PackResults(Skeleton skeleton)
        {
            var kinectBodyLandmarks = new PoseLandmarks();
            const int poselmListSize = 33;
            var poseLandmarks = new Landmark[poselmListSize];

            for (var jointId = 0; jointId < (int)JointId.Count; jointId++)
            {
                var joint = skeleton.GetJoint(jointId);
                var mpJointId = (int)LandmarkUtils.KinectJoint2MediapipeJoint((JointId)jointId);
                if (mpJointId < 0) continue;
                var lm = PackLandmark(joint);
                poseLandmarks[mpJointId] = lm;
            }
            for (var i = 0; i < poseLandmarks.Length; i++)
            {
                if (poseLandmarks[i] == null)
                    poseLandmarks[i] = new Landmark();
            }
            if(poseLandmarks != null && poseLandmarks.Length > 0)
                kinectBodyLandmarks.Landmarks.AddRange(poseLandmarks);

            _result.PoseLandmarks = kinectBodyLandmarks;
        }

        Landmark PackLandmark(Joint joint)
        {
            var lm = new Landmark();
             
            lm.X = joint.Position.X / 1000;
            lm.Y = joint.Position.Y / 1000;
            lm.Z = joint.Position.Z / 1000;
            lm.Confidence = joint.ConfidenceLevel switch
            {
                JointConfidenceLevel.None => 0f,
                JointConfidenceLevel.Low => 0.3f,
                JointConfidenceLevel.Medium => 0.6f,
                JointConfidenceLevel.High => 0.9f,
                _ => throw new InvalidOperationException()
            };

            return lm;
        }

        public void SendResults() 
        {
            var sendData = _result.ToByteArray();
            _sender.Send(sendData, sendData.Length);
        }

        public void Dispose()
        {
            _sender.Close(); _sender.Dispose();
            _receiver.Close(); _receiver.Dispose();
        }
    }
}
