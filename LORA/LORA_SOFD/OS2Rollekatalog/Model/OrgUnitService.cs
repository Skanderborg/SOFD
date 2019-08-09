using System;
using System.Collections.Generic;
using System.Linq;
using DAL_old;
using DAL_old.LORA_SOFD;
using System.Text;
using System.Threading.Tasks;

namespace OS2Rollekatalog.Model
{
    internal class OrgUnitService
    {
        private EmployeeService empService;
        private IRepo<Orgunit> orgRepo;

        internal OrgUnitService(string connStr)
        {
            orgRepo = new OrgunitRepo(connStr);
            empService = new EmployeeService(connStr);
        }

        internal OrgUnit GetOrgUnitFromID(int los_id)
        {
            Orgunit orgunit = orgRepo.Query.Where(o => o.Los_id == los_id).FirstOrDefault();
            if (orgunit != null)
            {
                OrgUnit _OrgUnit = new OrgUnit()
                {
                    uuid = orgunit.Uuid,
                    name = orgunit.Name,
                    employees = empService.GetEmployeesFromOrgId(los_id),
                    kle_interest = new List<string>(),
                    kle_performing = new List<string>(),
                    children = new List<OrgUnit>()
                };

                return _OrgUnit;
            }
            else
            {
                throw new Exception("Orgunit not found, id: " + los_id);
            }
        }

    }
}
