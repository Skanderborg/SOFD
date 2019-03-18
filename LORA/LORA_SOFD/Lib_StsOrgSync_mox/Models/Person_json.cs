using Newtonsoft.Json;

namespace Lib_StsOrgSync_mox.Models
{
    public class Person_json
    {
        [JsonProperty(PropertyName = "Name", Required = Required.Always)]
        public string Name { get; set; }
        [JsonProperty(PropertyName = "Cpr", Required = Required.Always)]
        public string Cpr { get; set; }
    }
}
