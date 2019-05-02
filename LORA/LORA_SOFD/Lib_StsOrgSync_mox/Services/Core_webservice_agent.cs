using System.Text;
using System.Net;

namespace Lib_StsOrgSync_mox.Services
{
    public class Core_webservice_agent
    {
        private string api_key;
        private string cvr;

        public Core_webservice_agent(string api_key, string cvr)
        {
            this.api_key = api_key;
            this.cvr = cvr;
        }

        public void PostOrganisation(string json_org, string endpoint)
        {
            using (var client = new WebClient_extension())
            {
                client.Headers[HttpRequestHeader.ContentType] = "application/json";
                client.Headers.Add("apiKey", api_key);
                client.Headers.Add("cvr", cvr);
                client.Encoding = Encoding.UTF8;
                client.UploadString(endpoint, "POST", json_org);
                var result = client.ResponseHeaders;
            }
        }

        public void PostUser(string json_org, string endpoint)
        {
            using (var client = new WebClient_extension())
            {
                client.Headers[HttpRequestHeader.ContentType] = "application/json";
                client.Headers.Add("apiKey", api_key);
                client.Headers.Add("cvr", cvr);
                client.Encoding = Encoding.UTF8;
                client.UploadString(endpoint, "POST", json_org);
                var result = client.ResponseHeaders;
            }
        }

        public bool DeleteOrganisation(string endpoint, string uuid)
        {
            string url = endpoint + "/" + uuid;
            WebRequest request = WebRequest.Create(url);
            request.Method = "DELETE";
            request.Headers.Add("apiKey", api_key);
            request.Headers.Add("cvr", cvr);
            request.Timeout = 15000;

            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            {
                if (response == null)
                    return false;
                else if (response.StatusCode == HttpStatusCode.OK)
                    return true;
                else
                    return false;
            }
        }

        public bool DeleteUser(string endpoint, string uuid)
        {
            string url = endpoint + uuid;
            WebRequest request = WebRequest.Create(url);
            request.Method = "DELETE";
            request.Headers.Add("apiKey", api_key);
            request.Headers.Add("cvr", cvr);
            request.Timeout = 15000;

            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            {
                if (response == null)
                    return false;
                else if (response.StatusCode == HttpStatusCode.OK)
                    return true;
                else
                    return false;
            }
        }
    }
}
