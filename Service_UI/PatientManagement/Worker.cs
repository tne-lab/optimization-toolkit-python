using log4net.Config;
using log4net;
using Python.Runtime;
using System.Diagnostics;
using NetMQ.Sockets;
using NetMQ;
using Newtonsoft.Json;
using System.Collections.Concurrent;
using static System.Runtime.InteropServices.JavaScript.JSType;
using System.Security.Policy;

namespace WSOPT
{
    public class Worker : BackgroundService
    {
        private readonly ILogger<Worker> _logger;
        private static BlockingCollection<string> dataQueue = new BlockingCollection<string>();
        private static readonly ILog log = LogManager.GetLogger(typeof(Program));

        public Worker(ILogger<Worker> logger)
        {
            _logger = logger;
            XmlConfigurator.Configure(new System.IO.FileInfo("log4net.config"));
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            
            while (!stoppingToken.IsCancellationRequested)
            {
                log.Info("Starting the ZMQ thread");
                ConfigurePython();
                initialization();
                OptimizationInitialize();
                string scriptDirectory = @"D:\Sumedh\Projects\Methods for psychiatric DBS programming\application\CSharpCode\DatabaseCode\WorkerServiceDRA\WSOPT\WSOPT"; 
                var zmqthreadPatient = Task.Run(() => Optimization(scriptDirectory));
                var zmqThreadPhysicianPubSub = Task.Run(() => Connectphysician());
                var zmqThreadPhysicianReqRep = Task.Run(() => PhysicianCommands());
                await Task.WhenAll(zmqthreadPatient, zmqThreadPhysicianPubSub, zmqThreadPhysicianReqRep);
            }
        }
        static void ConfigurePython()
        {
            log.Info("Configuring the location of the python");
            string pythonHome = @"C:\Python38";
            string pythonDll = System.IO.Path.Combine(pythonHome, "python38.dll");
            if (!System.IO.File.Exists(pythonDll))
            {
                log.Info($"Python DLL not found at {pythonDll}");
                return;
            }
            string pythonHomeEnv = Environment.GetEnvironmentVariable("PYTHONHOME");
            string pythonDllEnv = Environment.GetEnvironmentVariable("PYTHONNET_PYDLL");
            if(Environment.GetEnvironmentVariable("PYTHONHOME") == null || Environment.GetEnvironmentVariable("PYTHONNET_PYDLL") == null)
            {
                log.Info("Setting up location of the Python to Environment");
                Environment.SetEnvironmentVariable("PYTHONHOME", pythonHome);
                Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            }
            Runtime.PythonDLL = pythonDll;
        }

        static void initialization()
        {
            PythonEngine.Initialize();
            PythonEngine.BeginAllowThreads();
        }

        static void OptimizationInitialize()
        {
            using (Py.GIL())
            {
                // add here the code for restarting the application
            }
        }

        static void Optimization(string scriptDirectory)
        {

            // Initialize and use Python.NET
            using (Py.GIL())
            {
                // Ensure the directory exists
                if (!System.IO.Directory.Exists(scriptDirectory))
                {
                    Console.WriteLine($"Script directory not found at {scriptDirectory}");
                    return;
                }
                
                PythonEngine.Exec($"import sys; sys.path.append(r'{scriptDirectory}')");
               // Import the custom script
                dynamic numpyScript = Py.Import("numpy_script");
                dynamic SDMall = numpyScript.fetch_data();
                dynamic app = numpyScript.Application(10000, 15, 8, 1, 1, "noalgorithm", SDMall);



                // Initialize the startup configuration
                app.initialize_startup_configuration();
                Random random = new Random();
                using (var server = new ResponseSocket())
                {
                    Stopwatch stopwatch = new Stopwatch();
                    server.Bind("tcp://127.0.0.1:3002");
                    log.Debug("SERVER BINDING: Connection established between UI and database service.");
                    while (true)
                    {
                        string request = server.ReceiveFrameString();
                        log.Debug("Received from client: " + request);
                        dynamic responseObject = JsonConvert.DeserializeObject(request);
                        stopwatch.Restart();
                        // communication value
                        app.run_application((float)responseObject.RT, 1, (int)responseObject.trial);

                        //Console.WriteLine($"CS output after: {app.optimizationState["measured"]}");
                        int trial = app.optimizationState["trial"];
                        responseObject.RT = ((float)app.optimizationState["measured"][trial]).ToString();
                        responseObject.PatientRT = ((float)app.optimizationState["Gen_YRT_value"][trial]).ToString();
                        responseObject.StimulationSite = ((float)app.optimizationState["playArmSelected"][trial]).ToString();
                        responseObject.nextStim = ((float)app.optimizationState["armselected"]).ToString();
                        float nexttrial = trial+ 1;
                        Console.WriteLine("CS CODE: Current stimulation at "+ trial + "---" + responseObject.StimulationSite +  "Next stimulation at trial "+ nexttrial + " stim at " + responseObject.nextStim);
                        //B: Run stuff you want timed
                        stopwatch.Stop();
                        //Console.WriteLine($"Timestamp after: {stopwatch.ElapsedMilliseconds}, milliseconds");
                        // Send a response back to the client
                        dynamic responseVar = JsonConvert.SerializeObject(responseObject);
                        dataQueue.Add(responseVar);
                        string response = responseVar;
                        server.SendFrame(response);

                    }
                }


            }

        }
        static void PhysicianCommands()
        {
            using (var server = new ResponseSocket())
            {
                server.Bind("tcp://127.0.0.1:3097");
                Console.WriteLine("Req-Rep ZMQ Connections.");
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
        static void Connectphysician()
        {
            using (var publisher = new PublisherSocket())
            {
                publisher.Bind("tcp://127.0.0.1:3096");
                Console.WriteLine("Publisher sending data.");
                while (true)
                {
                    string response;
                    if (dataQueue.TryTake(out response)) {

                        // string response = dataQueue.Take();
                        publisher.SendFrame(response);
                        //Console.WriteLine("sending the data to physician screen");
                        //Console.WriteLine("Received request: " + response);

                    }
                }
            }

        }
    }
}
