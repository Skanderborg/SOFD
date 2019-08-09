using OS2Rollekatalog.Model;
using System.Linq;
using DAL_old;
using DAL_old.LORA_SOFD;

namespace OS2Rollekatalog.Service
{
    internal class OrgRecursionService
    {
        private OrgUnitService orgService;
        private IRepo<Orgunit> orgRepo;
        int parentOrgId;

        internal OrgRecursionService(string connStr, int parentOrgId)
        {
            orgService = new OrgUnitService(connStr);
            orgRepo = new OrgunitRepo(connStr);
            this.parentOrgId = parentOrgId;
        }

        internal OrgUnit GetTopOrgUnit()
        {
            OrgUnit result = orgService.GetOrgUnitFromID(parentOrgId);
            GetOrgUnitRecursion(result);
            return result;
        }

        private OrgUnit GetOrgUnitRecursion(OrgUnit org)
        {
            //lidt dobbeltkonfekt fordi vores SOFD ikke har parentOrgUUID, men det burde man nok
            int orgLos = orgRepo.Query.Where(o => o.Uuid == org.uuid).First().Los_id;
            IQueryable<Orgunit> query = orgRepo.Query.Where(o => o.Parent_losid == orgLos);

            if (query.Count() != 0)
            {
                foreach (Orgunit _org in query)
                {
                    OrgUnit child = orgService.GetOrgUnitFromID(_org.Los_id);
                    org.children.Add(child);
                    GetOrgUnitRecursion(child);
                }
            }
            return org;
        }

    }
}
