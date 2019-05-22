using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD
{
    public class AkubizRepo : IRepo<v_akubiz_employee>
    {
        LORA_SOFDDataContext c;

        public AkubizRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }

        public IQueryable<v_akubiz_employee> Query => c.v_akubiz_employees;

        public int Add(v_akubiz_employee e)
        {
            throw new NotImplementedException();
        }

        public void Delete(v_akubiz_employee e)
        {
            throw new NotImplementedException();
        }

        public void Update(v_akubiz_employee e)
        {
            throw new NotImplementedException();
        }
    }
}
