using System;
using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class ChangeRepo : IRepo<change>
    {
        private LORA_SOFDDataContext c;
        public ChangeRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }
        public IQueryable<change> Query => c.changes;

        public int Add(change e)
        {
            c.changes.InsertOnSubmit(e);
            c.SubmitChanges();
            return 0;
        }

        public void Delete(change e)
        {
            throw new NotImplementedException();
        }

        public void Update(change e)
        {
            throw new NotImplementedException();
        }
    }
}
