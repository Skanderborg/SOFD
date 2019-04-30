using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD
{
    public class ManagerLookupRepo : IRepo<Manager_lookup>
    {
        private LORA_SOFDDataContext c;
        public ManagerLookupRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }

        public IQueryable<Manager_lookup> Query => c.Manager_lookups;

        public int Add(Manager_lookup e)
        {
            c.Manager_lookups.InsertOnSubmit(e);
            Update(e);
            return e.system_id;
        }

        public void Delete(Manager_lookup e)
        {
            c.Manager_lookups.DeleteOnSubmit(e);
            Update(e);
        }

        public void Update(Manager_lookup e)
        {
            c.SubmitChanges();
        }
    }
}
