using Newtonsoft.Json;

namespace Lib_StsOrgSync_mox.Models
{
    public class Generic_adress_json
    {
        [JsonProperty(PropertyName = "Value", Required = Required.Always)]
        public string Value { get; set; }
    }
}
