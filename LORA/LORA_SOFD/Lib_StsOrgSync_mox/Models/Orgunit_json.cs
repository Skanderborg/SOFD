using Newtonsoft.Json;
using System;
using System.Collections.Generic;

namespace Lib_StsOrgSync_mox.Models
{
    public class Orgunit_json
    {
        [JsonProperty(PropertyName = "Uuid", Required = Required.Always)]
        public string Uuid { get; set; }

        [JsonProperty(PropertyName = "ShortKey", Required = Required.Always)]
        public string ShortKey { get; set; }

        [JsonProperty(PropertyName = "Name", Required = Required.Always)]
        public string Name { get; set; }

        [JsonProperty(PropertyName = "ParentOrgUnitUuid")]
        public string ParentOrgUnitUuid { get; set; }

        [JsonProperty(PropertyName = "Timestamp", Required = Required.Always)]
        public DateTime Timestamp { get; set; }

        [JsonProperty(PropertyName = "Phone", Required = Required.Always)]
        public Generic_adress_json Phone { get; set; }

        [JsonProperty(PropertyName = "Email", Required = Required.Always)]
        public Generic_adress_json Email { get; set; }

        [JsonProperty(PropertyName = "ItSystemUuids", Required = Required.Always)]
        public List<string> ItSystemUuids { get; set; }
    }
}
