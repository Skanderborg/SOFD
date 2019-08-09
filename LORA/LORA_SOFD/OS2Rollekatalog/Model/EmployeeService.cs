using System.Collections.Generic;
using System.Linq;
using DAL_old.LORA_SOFD;
using DAL_old;

namespace OS2Rollekatalog.Model
{
    internal class EmployeeService
    {
        private IRepo<v_sofd_medarbejderoverblik> empRepo;

        internal EmployeeService(string connStr)
        {
            empRepo = new Sofd_Medarbejderoverblik_Repo(connStr);
        }

        internal List<Employee> GetEmployeesFromOrgId(int orgId)
        {
            List<Employee> result = new List<Employee>();

            foreach (v_sofd_medarbejderoverblik emp in empRepo.Query.Where(e => e.Los_id == orgId))
            {
                Employee _emp = new Employee()
                {
                    uuid = emp.Uuid,
                    user_id = emp.UserId,
                    name = emp.Firstname + " " + emp.Lastname,
                    title = emp.position_name
                };
                result.Add(_emp);
            }

            return result;
        }
    }
}
