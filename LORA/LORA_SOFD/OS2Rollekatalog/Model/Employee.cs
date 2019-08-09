using Newtonsoft.Json;

namespace OS2Rollekatalog.Model
{
    internal class Employee
    {
        [JsonProperty(PropertyName = "uuid", Required = Required.Always)]
        internal string uuid { get; set; }

        [JsonProperty(PropertyName = "user_id", Required = Required.Always)]
        internal string user_id { get; set; }

        [JsonProperty(PropertyName = "name", Required = Required.Always)]
        internal string name { get; set; }

        [JsonProperty(PropertyName = "title", Required = Required.Always)]
        internal string title { get; set; }
    }
}
