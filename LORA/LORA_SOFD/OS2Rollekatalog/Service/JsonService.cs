using Newtonsoft.Json;
using OS2Rollekatalog.Model;
using System.Net;
using System.Text;

namespace OS2Rollekatalog.Service
{
    internal class JsonService
    {
        private OrgRecursionService rs;

        public JsonService(string connStr, int parentOrgId)
        {
            rs = new OrgRecursionService(connStr, parentOrgId);
        }

        public string GetJson()
        {
            OrgUnit org = rs.GetTopOrgUnit();
            return JsonConvert.SerializeObject(org);
        }

        public void PostJson(string apiKey, string endPointUrl)
        {
            string json = GetJson();

            byte[] bytes = Encoding.UTF8.GetBytes(json);
            json = Encoding.UTF8.GetString(bytes);

            using (var client = new WebClient())
            {
                client.Headers[HttpRequestHeader.ContentType] = "application/json";
                client.Headers.Add("ApiKey", apiKey);
                client.Encoding = Encoding.UTF8;
                client.UploadString(endPointUrl, "POST", json);
            }
        }
    }
}
