using System;
using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class QUserRepo : IRepoQueue<qUser>
    {
        private LORA_SOFDDataContext c;
        public QUserRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }
        public IQueryable<qUser> Query => c.qUsers;

        public long Add(qUser e)
        {
            c.qUsers.InsertOnSubmit(e);
            c.SubmitChanges();
            return e.System_id;
        }

        public void Delete(qUser e)
        {
            c.qUsers.DeleteOnSubmit(e);
            c.SubmitChanges();
        }

        public void Update(qUser e)
        {
            throw new NotImplementedException();
        }
    }
}
