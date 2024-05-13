using System;
using System.Collections.Generic;
using System.ServiceProcess;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;

namespace ZMQservice
{
    public partial class MyService : ServiceBase
    {
        private Dictionary<string, string> memoryState;
        private List<double> memoryStateHistory;

        public MyService()
        {
            //  InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            memoryState = new Dictionary<string, string>();
            memoryStateHistory = new List<double>();

            Thread clientHandlerThread = new Thread(HandleClient);
            clientHandlerThread.Start();
            Console.WriteLine("Service started.");
        }

        protected override void OnStop()
        {
            // Clean up resources here if necessary
        }

        private void HandleClient()
        {
            using (var server = new ResponseSocket())
            {
                server.Bind("tcp://127.0.0.1:3000");

                while (true)
                {
                    string request = server.ReceiveFrameString();
                    Console.WriteLine("Received: " + request);

                    double processedData;
                    if (double.TryParse(request, out processedData))
                    {
                        memoryStateHistory.Add(processedData);
                    }
                    else
                    {
                        processedData = 0; // Or handle the case when conversion fails
                    }

                    memoryState["processed_data"] = processedData.ToString();

                    server.SendFrame(memoryState["processed_data"]);
                    Console.WriteLine("Memory state at end of connection: " + string.Join(", ", memoryStateHistory));
                }
            }
        }
    }
}
