using System;
using System.Linq;

namespace DAL_old.DSA_SOFD
{
    public class EmployeeRepo : IRepo<v_emp>
    {
        private DSA_SOFDDataContext c;
        public EmployeeRepo(string constr)
        {
            c = new DSA_SOFDDataContext(constr);
        }
        public IQueryable<v_emp> Query => c.v_emps;

        public int Add(v_emp e)
        {
            throw new NotImplementedException();
        }

        public void Delete(v_emp e)
        {
            throw new NotImplementedException();
        }

        public void Update(v_emp e)
        {
            throw new NotImplementedException();
        }
    }
}
