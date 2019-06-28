using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD_QUEUE
{
    public class Ad_user_org_change_repo : IRepo<ad_user_org_change>
    {
        private lora_queueDataContext c;

        public Ad_user_org_change_repo(string constr)
        {
            c = new lora_queueDataContext(constr);
        }
        public IQueryable<ad_user_org_change> Query => c.ad_user_org_changes;

        public int Add(ad_user_org_change e)
        {
            c.ad_user_org_changes.InsertOnSubmit(e);
            Update(e);
            return e.System_id;
        }

        public void Delete(ad_user_org_change e)
        {
            throw new NotImplementedException();
        }

        public void Update(ad_user_org_change e)
        {
            c.SubmitChanges();
        }
    }
}
