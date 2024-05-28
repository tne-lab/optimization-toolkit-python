using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace WSDRA
{
        public class SessionInfo
        {
            [Key]
            [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
            public int Id { get; set; }

            public int trial { get; set; }

            public float ReactionTime { get; set; }
            public string? PatientRT { get; set; }
            public bool Accuracy { get; set; }

            public string? Trialtype { get; set; }
            public string? NumberResponded { get; set; }
            public string? StimulationSite { get; set; }
    }
}
