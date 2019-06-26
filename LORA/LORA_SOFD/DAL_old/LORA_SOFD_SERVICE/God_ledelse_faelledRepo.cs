using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD_SERVICE
{
    public class God_ledelse_faelledRepo : IRepo<v_god_ledelse_fælleden>
    {
        private Lora_serviceDataContext c;

        public God_ledelse_faelledRepo(string constr)
        {
            c = new Lora_serviceDataContext(constr);
        }
        public IQueryable<v_god_ledelse_fælleden> Query => c.v_god_ledelse_fælledens;

        public int Add(v_god_ledelse_fælleden e)
        {
            throw new NotImplementedException();
        }

        public void Delete(v_god_ledelse_fælleden e)
        {
            throw new NotImplementedException();
        }

        public void Update(v_god_ledelse_fælleden e)
        {
            throw new NotImplementedException();
        }
    }
}
