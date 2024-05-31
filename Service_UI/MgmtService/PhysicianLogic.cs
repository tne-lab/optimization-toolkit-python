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
    public class RequestPhysician
    {
        public string? CommandType { get; set; }
        public Dictionary<string, object>? Data { get; set; }
    }

    public class ResponsePhysician
    {
        public string? Status { get; set; }
        public string? Message { get; set; }
        public Dictionary<string, object>? Data { get; set; }
    }

    public partial class Worker : BackgroundService
    {
        private Dictionary<string, Func<RequestPhysician, ResponsePhysician>>? _commandHandlers;
        private void InitializeCommandHandlers()
        {
            _commandHandlers = new Dictionary<string, Func<RequestPhysician, ResponsePhysician>>
            {
                { "Initial Handshake", HandleDefault },
                { "Sensor fitting", HandleSensorFitting },
                { "Sensor selection", HandleSensorSelection },
                { "Task Configuration", HandleTaskConfiguration },
                { "Pause", HandlePause },
                { "Start", HandleStart },
                { "Add New Trails", HandleAddNewTrails },
                { "Fetch patient details", HandleFetchPatientDetails },
                { "Fetch RT data", HandleFetchRTData }
            };
        }

        // connecting to physician which is at 3057, but as a client
        private void Connectphysician()
        {
            using (var publisher = new PublisherSocket())
            {
                publisher.Bind(PHYSICIAN_UI_ZMQ_PUB_SUB_CONNECTION);

                while (true)
                {
                    string? response;
                    if (_physicianDataQueue.TryTake(out response))
                    {
                        publisher.SendFrame(response);
                        Console.WriteLine("PHYSICIAN PUBLISHED" + response);

                    }
                }
            }
        }

        private void PhysicianCommands()
        {
            using (var server = new ResponseSocket())
            {
                server.Bind(PHYSICIAN_UI_ZMQ_REQ_REP_CONNECTION);
                Console.WriteLine("Req-Rep ZMQ Connections.");
                while (true)
                {

                    string requestJson = server.ReceiveFrameString();
                    Console.WriteLine("PHYSICIAN: Received request: " + requestJson);

                    // Deserialize the request
                    var request = JsonConvert.DeserializeObject<RequestPhysician>(requestJson);

                    // Process the request
                    var response = ProcessRequest(request);

                    // Serialize the response
                    string responseJson = JsonConvert.SerializeObject(response);

                    // Send the response back to the client
                    server.SendFrame(responseJson);
                    Console.WriteLine("PHYSICIAN: Sent response: " + responseJson);
                }
            }
        }

        private ResponsePhysician ProcessRequest(RequestPhysician request)
        {
            if (_commandHandlers.TryGetValue(request.CommandType, out var handler))
            {
                return handler(request);
            }
            else
            {
                return new ResponsePhysician
                {
                    Status = "Error",
                    Message = "Unknown command type",
                    Data = new Dictionary<string, object>()
                };
            }
        }
    }
}
