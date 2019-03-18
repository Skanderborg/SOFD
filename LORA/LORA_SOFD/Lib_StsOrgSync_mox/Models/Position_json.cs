using Newtonsoft.Json;

namespace Lib_StsOrgSync_mox.Models
{
    public class Position_json
    {
        [JsonProperty(PropertyName = "OrgUnitUuid", Required = Required.Always)]
        public string OrgUnitUuid { get; set; }

        [JsonProperty(PropertyName = "ShortKey", Required = Required.Always)]
        public string ShortKey { get; set; }

        [JsonProperty(PropertyName = "Name", Required = Required.Always)]
        public string Name { get; set; }
    }
}
