using log4net.Config;
using log4net;
using Python.Runtime;
using System.Diagnostics;
using System.Collections.Concurrent;
using Newtonsoft.Json;
using NetMQ;
using NetMQ.Sockets;
using System.Security.Policy;

namespace MANAGEMENTSERVICE
{
    public partial class Worker : BackgroundService
    {
        private void Databasethread()
        {
            Console.WriteLine("Database thread activated.");
            // ZeroMQ server logic
            using (var client = new RequestSocket())
            {
                client.Connect(DATABASE_ZMQ_CONNECTION);
                while (true)
                {
                    string? request;
                    if (_databaseDataQueue.TryTake(out request))
                    {
                        client.SendFrame(request);
                        Console.WriteLine("DATABASE DATA RECEIVED BACK" + request);
                        // Receive the response from the server
                        string response = client.ReceiveFrameString();

                    }
                }

            }
        }
    }
}
