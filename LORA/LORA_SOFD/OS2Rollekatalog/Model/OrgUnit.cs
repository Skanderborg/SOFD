using Newtonsoft.Json;
using System.Collections.Generic;

namespace OS2Rollekatalog.Model
{
    internal class OrgUnit
    {
        [JsonProperty(PropertyName = "uuid", Required = Required.Always)]
        internal string uuid { get; set; }

        [JsonProperty(PropertyName = "name", Required = Required.Always)]
        internal string name { get; set; }

        [JsonProperty(PropertyName = "employees")]
        internal List<Employee> employees { get; set; }

        [JsonProperty(PropertyName = "kle-performing")]
        internal List<string> kle_performing { get; set; }

        [JsonProperty(PropertyName = "kle-interest")]
        internal List<string> kle_interest { get; set; }

        [JsonProperty(PropertyName = "children")]
        internal List<OrgUnit> children { get; set; }
    }
}
