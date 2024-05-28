using log4net.Core;
using log4net.Layout;
using Newtonsoft.Json;
using System.IO;

namespace WSOPT
{
    public class JsonLayout : LayoutSkeleton
    {
        public override void ActivateOptions()
        {
            // No options to activate
        }

        public override void Format(TextWriter writer, LoggingEvent loggingEvent)
        {
            var logObject = new
            {
                Timestamp = loggingEvent.TimeStamp,
                Level = loggingEvent.Level.DisplayName,
                Logger = loggingEvent.LoggerName,
                Thread = loggingEvent.ThreadName,
                Message = loggingEvent.RenderedMessage,
                Exception = loggingEvent.ExceptionObject?.ToString()
            };

            var json = JsonConvert.SerializeObject(logObject);
            writer.WriteLine(json);
        }
    }
}
