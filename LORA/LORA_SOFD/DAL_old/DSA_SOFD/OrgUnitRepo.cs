using System;
using System.Linq;

namespace DAL_old.DSA_SOFD
{
    public class OrgUnitRepo : IRepo<OrgUnit>
    {
        DSA_SOFDDataContext context;

        public OrgUnitRepo(string constr)
        {
            context = new DSA_SOFDDataContext(constr);
        }

        public IQueryable<OrgUnit> Query => context.OrgUnits;

        public int Add(OrgUnit e)
        {
            throw new NotImplementedException();
        }

        public void Delete(OrgUnit e)
        {
            throw new NotImplementedException();
        }

        public void Update(OrgUnit e)
        {
            throw new NotImplementedException();
        }
    }
}
