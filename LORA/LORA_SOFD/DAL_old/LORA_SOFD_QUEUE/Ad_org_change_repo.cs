using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD_QUEUE
{
    public class Ad_org_change_repo : IRepo<ad_org_action>
    {
        private lora_queueDataContext c;

        public Ad_org_change_repo(string constr)
        {
            c = new lora_queueDataContext(constr);
        }
        public IQueryable<ad_org_action> Query => c.ad_org_actions;

        public int Add(ad_org_action e)
        {
            c.ad_org_actions.InsertOnSubmit(e);
            Update(e);
            return -1;
        }

        public void Delete(ad_org_action e)
        {
            throw new NotImplementedException();
        }

        public void Update(ad_org_action e)
        {
            c.SubmitChanges();
        }
    }
}
