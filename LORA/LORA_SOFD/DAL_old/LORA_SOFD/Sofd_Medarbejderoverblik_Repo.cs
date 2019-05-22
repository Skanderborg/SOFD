using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old.LORA_SOFD
{
    public class Sofd_Medarbejderoverblik_Repo : IRepo<v_sofd_medarbejderoverblik>
    {
        private LORA_SOFDDataContext c;

        public Sofd_Medarbejderoverblik_Repo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
        }
        public IQueryable<v_sofd_medarbejderoverblik> Query => c.v_sofd_medarbejderoverbliks;

        public int Add(v_sofd_medarbejderoverblik e)
        {
            throw new NotImplementedException();
        }

        public void Delete(v_sofd_medarbejderoverblik e)
        {
            throw new NotImplementedException();
        }

        public void Update(v_sofd_medarbejderoverblik e)
        {
            throw new NotImplementedException();
        }
    }
}
