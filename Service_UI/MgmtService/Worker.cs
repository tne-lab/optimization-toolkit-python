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

        private static readonly ILog log = LogManager.GetLogger(typeof(Program));

        // using single blocking collection does not work as it leads to data loss.
        private static BlockingCollection<string> _databaseDataQueue = new BlockingCollection<string>();
        private static BlockingCollection<string> _physicianDataQueue = new BlockingCollection<string>();

        // python application variable to interact with the code
        private dynamic? _numpyScript;
        private dynamic? _app;
        private dynamic? _calibration;
        private dynamic? _sensorModel;

        // private variable but treating them essentially as constant - all caps
        private readonly string DATABASE_ZMQ_CONNECTION;
        private readonly string PATIENT_UI_ZMQ_CONNECTION;
        private readonly string PHYSICIAN_UI_ZMQ_REQ_REP_CONNECTION;
        private readonly string PHYSICIAN_UI_ZMQ_PUB_SUB_CONNECTION;
        private readonly string SCRIPT_DIRECTORY;

        public Worker(ILogger<Worker> logger, IConfiguration configuration)
        {
            XmlConfigurator.Configure(new System.IO.FileInfo("log4net.config"));
            DATABASE_ZMQ_CONNECTION = configuration.GetConnectionString("DATABASE_ZMQ_CONNECTION") ?? string.Empty;
            PATIENT_UI_ZMQ_CONNECTION = configuration.GetConnectionString("PATIENT_UI_ZMQ_CONNECTION") ?? string.Empty;
            PHYSICIAN_UI_ZMQ_REQ_REP_CONNECTION = configuration.GetConnectionString("PHYSICIAN_UI_ZMQ_REQ_REP_CONNECTION") ?? string.Empty;
            PHYSICIAN_UI_ZMQ_PUB_SUB_CONNECTION = configuration.GetConnectionString("PHYSICIAN_UI_ZMQ_PUB_SUB_CONNECTION") ?? string.Empty;
            SCRIPT_DIRECTORY = configuration.GetConnectionString("SCRIPT_DIRECTORY") ?? string.Empty;
            InitializeCommandHandlers();
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                log.Info("ExecuteAsync: Initialization Communication threads");
                PythonEnvironmentSetup();
                PythonRuntimeInitialization();
                ScriptsInitialization();
                // Using Task - which provides high level abstraction of threads, improves concurrency
                var patientTask = Task.Run(() => TaskOptimization());
                var physicianPubSubTask = Task.Run(() => Connectphysician());
                var physicianReqRepTask = Task.Run(() => PhysicianCommands());
                var databaseTask = Task.Run(() => Databasethread());

                // Making sure all the task are finished before the end of the program
                await Task.WhenAll(physicianPubSubTask, physicianReqRepTask, databaseTask);
            }
        }

        static void PythonEnvironmentSetup()
        {
            log.Info("PythonEnvironmentSetup: Setting up python environment.");
            // setting the location of the python and dll
            string pythonHome = @"C:\Python38";
            string pythonDll = System.IO.Path.Combine(pythonHome, "python38.dll");
            if (!System.IO.File.Exists(pythonDll))
            {
                log.Info($"PYTHON SETUP: Python DLL not found at {pythonDll}");
                return;
            }

            // if the environment does not have the information, set the infomration
            if (Environment.GetEnvironmentVariable("PYTHONHOME") == null || Environment.GetEnvironmentVariable("PYTHONNET_PYDLL") == null)
            {
                log.Info("PYTHON SETUP: Set environment variable");
                Environment.SetEnvironmentVariable("PYTHONHOME", pythonHome);
                Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", pythonDll);
            }
        }

        static void PythonRuntimeInitialization()
        {
            log.Info("PythonRuntimeInitialization: Setting up python interpretor, library for python code execution.");
            // sets up python interpretor, library and python code execution
            PythonEngine.Initialize();
            // Allowing multiple threads to access python from .net
            PythonEngine.BeginAllowThreads();
        }

        private void ScriptsInitialization()
        {
            using (Py.GIL())
            {
                // Ensure the directory exists
                if (!System.IO.Directory.Exists(SCRIPT_DIRECTORY))
                {
                    Console.WriteLine($"Script directory not found at {SCRIPT_DIRECTORY}");
                    return;
                }
                PythonEngine.Exec($"import sys; sys.path.append(r'{SCRIPT_DIRECTORY}')");

                // Import the custom script
                _numpyScript = Py.Import("numpy_script");
            }
        }

    }
}
