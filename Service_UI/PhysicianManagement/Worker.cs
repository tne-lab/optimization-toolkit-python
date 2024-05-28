// dotnet build .\WSDRA.csproj
// dotnet run .\WSDRA.csproj
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;

namespace WSPHY
{
    public class Worker : BackgroundService
    {
        private readonly ILogger<Worker> _logger;
        private static BlockingCollection<string> dataQueue = new BlockingCollection<string>();
        public Worker(ILogger<Worker> logger)
        {
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                // Creating ZMQ thread
                var patientDataThread = Task.Run(() => PatientDataThread());
                var patientCommandThread = Task.Run(() => PatientCommandThread());
                var dBthread = Task.Run(() => DatabaseSaveThread());
                var physicianUIThread = Task.Run(() => PhysicianScreen());
                await Task.WhenAll(patientCommandThread, patientCommandThread, dBthread);
            }
        }

        // client logic to receive data from the management service to show it on the physician screen
        static void PatientDataThread()
        {
            // ZeroMQ server logic
            using (var subscriber = new SubscriberSocket())
            {
                subscriber.Connect("tcp://127.0.0.1:3096");
                subscriber.Subscribe("");
                Console.WriteLine("SERVER BINDING: Connection established between UI and database service.");
                while (true)
                {
                    string request = subscriber.ReceiveFrameString();
                    Console.WriteLine("Received from client: " + request);

                    dataQueue.Add(request);
                }
            }
        }

        // client logic to connect to the management service on the patient's computer to convey commands
        // Different 
        static void PatientCommandThread()
        {
            // ZeroMQ server logic
            using (var client = new RequestSocket())
            {
                client.Connect("tcp://127.0.0.1:3097");
                Console.WriteLine("SERVER BINDING ZMQ COMMANDS CONNECTED .");
                string request = "COMMAND CHANGE THIS";

                // Send the request to the server
                client.SendFrame(request);

                // Receive the response from the server
                string response = client.ReceiveFrameString();
                Console.WriteLine("Client: Received response: " + response);
            }
        }

        /// <summary>
        /// "htps://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff649690(v=pandp.10)?redirectedfrom=MSDN///"
        /// </summary>
        static void DatabaseSaveThread()
        {
            while (true)
            {
                // Take the next item from the queue (blocking if necessary)
                string request = dataQueue.Take();
                Console.WriteLine("Processing and saving to database: " + request);

                // Process and save the request to the database
                // ProcessRequest(request); // this part updates the table.
            }
        }

        static void ProcessRequest(string request)
        {
            using (var dbContext = new DRADbContext())
            {
                var sessionInfo = new Repository<SessionInfo>(dbContext);

                // dynamic only because this gives freedom for the data structure
                dynamic responseObject = JsonConvert.DeserializeObject(request);

                if (responseObject.DataType == "PatientData")
                {
                    if (dbContext.IsDatabaseConnected())
                    {
                        try
                        {

                            var session = new SessionInfo { trial = responseObject.trial, ReactionTime = responseObject.RT, Accuracy = responseObject.Response, Trialtype = responseObject.Trialtype, NumberResponded = responseObject.NumberResponded, StimulationSite = responseObject.StimulationSite, PatientRT = responseObject.PatientRT };
                            sessionInfo.AddSample(session);
                            Console.WriteLine("DATABASE CONNECTION: Database connected and data saved.");
                        }
                        catch
                        {
                            Console.WriteLine("DATABASE CONNECTION: Database connected and data not saved.");
                            Console.WriteLine("Error");
                        }

                    }
                    else
                    {
                        Console.WriteLine("Database not connected");
                    }
                }
                else if (responseObject.DataType == "InitiationData")
                {
                    Console.WriteLine("Processing request: " + responseObject.MessageSend);
                }
            }

        }

        static void PhysicianScreen()
        {
            using (var server = new ResponseSocket())
            {
                server.Bind("tcp://127.0.0.1:3057");
                Console.WriteLine("Req-Rep ZMQ Connection with the Physician UI.");
                while (true)
                {

                    string request = server.ReceiveFrameString();
                    Console.WriteLine("Server: Received request: " + request);

                    // Process the request (e.g., perform some computation)
                    string response = "Server: Processed request: " + request;

                    // Send the response back to the client
                    server.SendFrame(response);
                    Console.WriteLine("Server: Sent response: " + response);
                }
            }
        }
    }
}
