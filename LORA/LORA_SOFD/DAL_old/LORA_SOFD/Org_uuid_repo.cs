using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DAL_old;

namespace DAL_old.LORA_SOFD
{
    public class Org_uuid_repo : IRepo<org_uiid>
    {
        private LORA_SOFDDataContext c;

        public Org_uuid_repo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }

        public IQueryable<org_uiid> Query => c.org_uiids;

        public int Add(org_uiid e)
        {
            throw new NotImplementedException();
        }

        public void Delete(org_uiid e)
        {
            throw new NotImplementedException();
        }

        public void Update(org_uiid e)
        {
            throw new NotImplementedException();
        }
    }
}
