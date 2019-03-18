using Newtonsoft.Json;
using System.Collections.Generic;

namespace Lib_StsOrgSync_mox.Models
{
    public class User_json
    {
        [JsonProperty(PropertyName = "Uuid", Required = Required.Always)]
        public string Uuid { get; set; }

        [JsonProperty(PropertyName = "UserId", Required = Required.Always)]
        public string UserId { get; set; }

        [JsonProperty(PropertyName = "Location", Required = Required.Always)]
        public Generic_adress_json Location { get; set; }

        [JsonProperty(PropertyName = "Email", Required = Required.Always)]
        public Generic_adress_json Email { get; set; }

        [JsonProperty(PropertyName = "Positions", Required = Required.Always)]
        public List<Position_json> Positions { get; set; }

        [JsonProperty(PropertyName = "Person", Required = Required.Always)]
        public Person_json Person { get; set; }
    }
}
