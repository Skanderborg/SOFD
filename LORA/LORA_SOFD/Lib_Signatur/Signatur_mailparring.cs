using DAL_old;
using DAL_old.LORA_SOFD;
using MDMSOFD;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lib_Signatur
{
    public class Signatur_mailparring
    {
        private IRepo<Position> posRepo = new PositionRepo("Data Source=dbsrv_lora_sofd;Initial Catalog=LORA_SOFD;User ID=lora_sofd_rw;Password=gGU4pvePn5M2fTUEQpPgWRPSCWDUn2");
        private IRepo<Orgunit> orgRepo = new OrgunitRepo("Data Source=dbsrv_lora_sofd;Initial Catalog=LORA_SOFD;User ID=lora_sofd_rw;Password=gGU4pvePn5M2fTUEQpPgWRPSCWDUn2");
        private signatur_tmp_repo mdmRepo = new signatur_tmp_repo();

        public void wooot()
        {

            foreach (Position pos in posRepo.Query.Where(p => p.User_fk != null && p.User.Email.Length > 1))
            {
                if (pos.User.Email != null)
                {
                    string orgname;
                    if (pos.Orgunit.Org_niveau == 4)
                        orgname = pos.Orgunit.Name;
                    else if (pos.Orgunit.Org_niveau < 4)
                        orgname = "Direktion";
                    else
                        orgname = OrgNameRecursion(pos.Orgunit);

                    signatur_tmp sig = new signatur_tmp()
                    {
                        skabelongruppe = orgname,
                        email = pos.User.Email,
                    };
                    mdmRepo.Add(sig);
                }
            }
        }

        private string OrgNameRecursion(Orgunit org)
        {

            if (org.Org_niveau == 4)
                return org.Name;
            else
                return OrgNameRecursion(orgRepo.Query.Where(o => o.Los_id == org.Parent_losid).First());

        }
    }
}
