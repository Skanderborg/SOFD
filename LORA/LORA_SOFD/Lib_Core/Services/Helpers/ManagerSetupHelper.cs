using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DAL_old;
using DAL_old.LORA_SOFD;

namespace Lib_Core.Services.Helpers
{
    public class ManagerSetupHelper
    {
        private IRepo<Manager_lookup> mlRepo;
        private IRepo<Position> posRepo;
        private IRepo<Orgunit> orgRepo;

        public ManagerSetupHelper(string constr)
        {
            mlRepo = new ManagerLookupRepo(constr);
            posRepo = new PositionRepo(constr);
            orgRepo = new OrgunitRepo(constr);
        }

        private void Delte_Manager_Lookups()
        {
            foreach(Manager_lookup ml in mlRepo.Query)
            {
                if (posRepo.Query.Where(p => p.Opus_id == ml.opus_id).Count() == 0)
                {
                    mlRepo.Delete(ml);
                }
            }
        }

        private void Update_Manager_Lookups()
        {
            foreach (Position pos in posRepo.Query.Where(p => p.Last_changed > DateTime.Now.AddDays(-3)))
            {

            }
        }

        private int GetNearestManagerOpusId()
        {
            
        }

    }
}
