using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using akubiz_lib.Models;
using DAL_old;
using DAL_old.LORA_SOFD;

namespace akubiz_lib
{
    public class EmployeeService
    {
        IRepo<v_akubiz_employee> akubizRepo;
        IRepo<Position> posRepo;

        public EmployeeService(string lora_constr)
        {
            akubizRepo = new AkubizRepo(lora_constr);
            posRepo = new PositionRepo(lora_constr);
        }

        public string GetEmployeeCSV()
        {
            List<Akubiz_Emp> emplist = new List<Akubiz_Emp>();
            foreach(v_akubiz_employee vae in akubizRepo.Query)
            {
                string manager = "";
                manager = posRepo.Query.Where(p => p.Opus_id == vae.manager_opus_id).First().User_fk;
                emplist.Add(new Akubiz_Emp
                {
                    uuid = vae.User_fk,
                    fullname = vae.Name,
                    ad1 = vae.UserId,
                    ad2 = vae.UserId,
                    ad3 = vae.UserId,
                    manager_uuid = manager,
                    email = vae.Email,
                    underligtnummer = "?",
                    los_id1 = vae.Orgunit_losid_fk.ToString(),
                    los_id2 = vae.Orgunit_losid_fk.ToString(),
                    cpr1 = vae.Person_fk,
                    cpr2 = vae.Person_fk,
                    nul = "0"
                });
            }

            IEnumerable<string> res = emplist.Select(e => String.Join(";", e.uuid, e.fullname, e.ad1, e.ad2, e.ad3, e.manager_uuid, e.email, e.underligtnummer, e.los_id1, e.los_id2,
                e.cpr1, e.cpr2, e.nul));
            return String.Join(Environment.NewLine, res);
        }

    }
}
