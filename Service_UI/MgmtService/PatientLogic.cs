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
        private void TaskOptimization()
        {
            // Initialize and use Python.NET
            using (var server = new ResponseSocket())
            {
                Random random = new Random();

                server.Bind(PATIENT_UI_ZMQ_CONNECTION);
                log.Info("SERVER BINDING: Connection established between UI and database service.");
                while (true)
                {
                    string request = server.ReceiveFrameString();
                    log.Debug("Received from client: " + request);
                    dynamic responseObject = JsonConvert.DeserializeObject(request)!;
                    string response;
                    if (responseObject != null)
                    {
                        if (responseObject.DataType == "InitiationData")
                        {
                            Console.WriteLine("Processing request: " + responseObject.MessageSend);
                            response = "Server received and processed: " + request.ToUpper();
                        }
                        else
                        {
                            using (Py.GIL())
                            {
                                // Run application class object
                                _app.run_application((float)responseObject.RT, 1, (int)responseObject.trial);
                                int trial = _app.optimizationState["trial"];
                                responseObject.RT = ((float)_app.optimizationState["measured"][trial]).ToString();
                                responseObject.PatientRT = ((float)_app.optimizationState["Gen_YRT_value"][trial]).ToString();
                                responseObject.StimulationSite = ((float)_app.optimizationState["playArmSelected"][trial]).ToString();
                                responseObject.nextStim = ((float)_app.optimizationState["armselected"]).ToString();

                                float nexttrial = trial + 1;
                                Console.WriteLine("CS CODE: Current stimulation at " + trial + "-" + responseObject.StimulationSite + "Next stimulation at trial " + nexttrial + " stim at " + responseObject.nextStim);
                                dynamic responseVar = JsonConvert.SerializeObject(responseObject);
                                _physicianDataQueue.Add(responseVar);
                                _databaseDataQueue.Add(responseVar);
                                response = responseVar;
                            }
                        }
                        server.SendFrame(response);
                    }
                }



            }
        }
    }
}
