using System;
using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class QADRepo : IRepo<qUsers_AD>
    {
        private LORA_SOFDDataContext c;

        public QADRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }
        public IQueryable<qUsers_AD> Query => c.qUsers_ADs;

        public int Add(qUsers_AD e)
        {
            c.qUsers_ADs.InsertOnSubmit(e);
            c.SubmitChanges();
            return e.System_id;
        }

        public void Delete(qUsers_AD e)
        {
            throw new NotImplementedException();
        }

        public void Update(qUsers_AD e)
        {
            throw new NotImplementedException();
        }
    }
}
