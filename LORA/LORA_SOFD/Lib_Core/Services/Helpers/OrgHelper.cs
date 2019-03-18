using DAL_old;
using DAL_old.LORA_SOFD;
using MDMSOFD;
using System.Linq;

namespace Lib_Core.Services.Helpers
{
    public class OrgHelper
    {
        private IRepo<Orgunit> lora_orgRepo;

        public OrgHelper(string lora_constr)
        {
            lora_orgRepo = new OrgunitRepo(lora_constr);
        }

        public void SetOrgUIDS()
        {
            mdmsofd m = new mdmsofd();

            foreach(Orgunit org in lora_orgRepo.Query)
            {
                org.Uuid = m.orgs.Where(mups => mups.OrgOpusID.Equals(org.Los_id.ToString())).First().orguuid;
                lora_orgRepo.Update(org);
            }
        }
    }
}
