using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD_SERVICE
{
    public class God_ledelse_pnrRepo : IRepo<god_ledelse_pnr>
    {
        private Lora_serviceDataContext c;

        public God_ledelse_pnrRepo(string constr)
        {
            c = new Lora_serviceDataContext(constr);
        }

        public IQueryable<god_ledelse_pnr> Query => c.god_ledelse_pnrs;

        public int Add(god_ledelse_pnr e)
        {
            c.god_ledelse_pnrs.InsertOnSubmit(e);
            Update(e);
            return e.system_id;
        }

        public void Delete(god_ledelse_pnr e)
        {
            c.god_ledelse_pnrs.DeleteOnSubmit(e);
            c.SubmitChanges();
        }

        public void Update(god_ledelse_pnr e)
        {
            c.SubmitChanges();
        }
    }
}
