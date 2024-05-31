using log4net.Config;
using log4net;
using Python.Runtime;
using System.Diagnostics;
using System.Collections.Concurrent;
using Newtonsoft.Json;
using NetMQ;
using NetMQ.Sockets;
using System.Security.Policy;
using static System.Net.Mime.MediaTypeNames;


namespace MANAGEMENTSERVICE
{
    public partial class Worker : BackgroundService
    {
        private ResponsePhysician HandleDefault(RequestPhysician request)
        {
            // Implement Sensor fitting logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Sensor fitting",
                Data = new Dictionary<string, object> { { "result", "Sensor fitting completed" } }
            };
        }

        private ResponsePhysician HandleSensorFitting(RequestPhysician request)
        {
            // Implement Sensor fitting logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Sensor fitting",
                Data = new Dictionary<string, object> { { "result", "Sensor fitting completed" } }
            };
        }

        private ResponsePhysician HandleSensorSelection(RequestPhysician request)
        {
            // Implement Sensor selection logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Sensor selection",
                Data = new Dictionary<string, object> { { "result", "Sensor selection completed" } }
            };
        }

        private ResponsePhysician HandleTaskConfiguration(RequestPhysician request)
        {
            Console.WriteLine("Configuration " + request.Data["trialNumber"] + " " + request.Data["blockSize"] + " " + request.Data["algorithm"]);
            ApplicationSensorModel();
            ApplicationObjectSetup((long)request.Data["trialNumber"], (long)request.Data["blockSize"], (string)request.Data["algorithm"]);
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Task Configuration",
                Data = new Dictionary<string, object> { { "result", "Configuration " + request.Data["trialNumber"] + " " + request.Data["blockSize"] + " " + request.Data["algorithm"] } }
            };
        }

        private ResponsePhysician HandlePause(RequestPhysician request)
        {
            // Implement Pause logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Pause",
                Data = new Dictionary<string, object> { { "result", "Pause completed" } }
            };
        }

        private ResponsePhysician HandleStart(RequestPhysician request)
        {
            // Implement Start logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Start",
                Data = new Dictionary<string, object> { { "result", "Start completed" } }
            };
        }

        private ResponsePhysician HandleAddNewTrails(RequestPhysician request)
        {
            // Implement Add New Trails logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Add New Trails",
                Data = new Dictionary<string, object> { { "result", "New Trails added" } }
            };
        }

        private ResponsePhysician HandleFetchPatientDetails(RequestPhysician request)
        {
            // Implement Fetch patient details logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Fetch patient details",
                Data = new Dictionary<string, object> { { "result", "Patient details fetched" } }
            };
        }

        private ResponsePhysician HandleFetchRTData(RequestPhysician request)
        {
            // Implement Fetch RT data logic
            return new ResponsePhysician
            {
                Status = "Success",
                Message = "Processed command: Fetch RT data",
                Data = new Dictionary<string, object> { { "result", "RT data fetched" } }
            };
        }


        // This is the code that will go in the handlers
        private void OptimizationSensorModelSelection(dynamic sensorModel)
        {
            _sensorModel = sensorModel;
        }

        private void ApplicationObjectSetup(long trialNumber, long blockSize, string algorithm)
        {using (Py.GIL()) { 
                // setup the entire application code
                _app = _numpyScript.Application(trialNumber, blockSize, 8, 1, 1, algorithm, _sensorModel);
            // Initialize the startup configuration
            _app.initialize_startup_configuration();
            }
        }

        private void CalibrationObjectSetup()
        {
            // if this is configurable add argument to the function
            _calibration = _numpyScript.Calibration(250);
        }

        private void ApplicationSensorModel()
        {
            using (Py.GIL())
            {
                _sensorModel = _numpyScript.fetch_data();
            }
        }


    }
}
