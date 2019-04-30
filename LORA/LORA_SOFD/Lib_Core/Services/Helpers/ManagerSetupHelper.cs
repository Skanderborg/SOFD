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

        public void Handle_Manager_Lookups()
        {
            Delte_Manager_Lookups();
            Update_Manager_Lookups();
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
                int manager_opus_id;
                // er det borgmesteren?
                if (pos.Orgunit_losid_fk == 1031023)
                    manager_opus_id = pos.Opus_id;
                // er medarbejderen selv leder? Så skal vi kigge 1 org op
                else if (pos.Is_Manager)
                    manager_opus_id = GetNearestManagerOpusIdRecursion(pos.Orgunit.Parent_losid);
                else
                    manager_opus_id = GetNearestManagerOpusIdRecursion(pos.Orgunit_losid_fk);

                Manager_lookup ml = mlRepo.Query.Where(m => m.opus_id == pos.Opus_id).FirstOrDefault();
                if (ml == null)
                {
                    ml = new Manager_lookup();
                    ml.opus_id = pos.Opus_id;
                    mlRepo.Add(ml);
                }
                ml.manager_opus_id = manager_opus_id;
                mlRepo.Update(ml);
            }
        }

        /// <summary>
        /// OBS: Hvis medarbejderen selv er leder, skal parent org være den første, hvis medarbejderen er medarbejder skal det være medarbejderens egen org
        /// OBS: borgmester, skal være sin egen leder!
        /// </summary>
        /// <param name="org_los_id"></param>
        /// <returns></returns>
        private int GetNearestManagerOpusIdRecursion(int org_los_id)
        {
            if (HasManager(org_los_id))
                return posRepo.Query.Where(p => p.Orgunit_losid_fk == org_los_id && p.Is_Manager).First().Opus_id;
            else
            {
                return GetNearestManagerOpusIdRecursion(orgRepo.Query.Where(o => o.Los_id == org_los_id).First().Parent_losid);
            }
        }

        private bool HasManager(int org_los_id)
        {
            return posRepo.Query.Where(p => p.Orgunit_losid_fk == org_los_id && p.Is_Manager).Count() == 1;
        }

    }
}
