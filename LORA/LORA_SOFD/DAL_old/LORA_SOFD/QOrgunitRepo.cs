using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class QOrgunitRepo : IRepoQueue<qOrgunit>
    {
        LORA_SOFDDataContext c;

        public QOrgunitRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }
        public IQueryable<qOrgunit> Query => c.qOrgunits;

        public long Add(qOrgunit e)
        {
            c.qOrgunits.InsertOnSubmit(e);
            c.SubmitChanges();
            return e.system_id;
        }

        public void Delete(qOrgunit e)
        {
            c.qOrgunits.DeleteOnSubmit(e);
            c.SubmitChanges();
        }

        public void Update(qOrgunit e)
        {
            c.SubmitChanges();
        }
    }
}
