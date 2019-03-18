using Lib_StsOrgSync_mox.Models;
using Newtonsoft.Json;

namespace Lib_StsOrgSync_mox.Services
{
    public class JsonService
    {

        public string Get_orgunit_json(Orgunit_json org)
        {
            return JsonConvert.SerializeObject(org);
        }

        public string Get_user_json(User_json org)
        {
            return JsonConvert.SerializeObject(org);
        }

    }
}
