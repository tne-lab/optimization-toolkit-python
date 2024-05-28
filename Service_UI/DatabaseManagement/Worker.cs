// dotnet build .\WSDRA.csproj
// dotnet run .\WSDRA.csproj
using System.Collections.Concurrent;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;

namespace WSDRA
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
                var zmqthread = Task.Run(() => ServerThread());

                //Creating database saving thread
                var dBthread = Task.Run(() => DatabaseSaveThread());

                // both the threads will complete what they were doing before closing,
                // required so as to avoid any data loss.
                await Task.WhenAll(zmqthread, dBthread);
            }
        }

        static void ServerThread()
        {
            // ZeroMQ server logic
            using (var server = new ResponseSocket())
            {
                server.Bind("tcp://127.0.0.1:3000");
                Console.WriteLine("SERVER BINDING: Connection established between UI and database service.");
                while (true)
                {
                    string request = server.ReceiveFrameString();
                    Console.WriteLine("Received from client: " + request);

                    dataQueue.Add(request);

                    // Send a response back to the client
                    string response = "Server received and processed: " + request.ToUpper();
                    server.SendFrame(response);
                }
            }
        }
        /// <summary>
        /// "htps://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff649690(v=pandp.10)?redirectedfrom=MSDN///"
        /// </summary>
        static void DatabaseSaveThread()
        {
            while (true)
            {
                // 
                // Take the next item from the queue (blocking if necessary)
                string request = dataQueue.Take();
                Console.WriteLine("Processing and saving to database: " + request);

                // Process and save the request to the database
                ProcessRequest(request);
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
    }
}
