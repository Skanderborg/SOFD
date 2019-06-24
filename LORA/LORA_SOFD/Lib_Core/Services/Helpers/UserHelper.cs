//using DAL_old;
//using DAL_old.LORA_SOFD;
//using MDMSOFD;
//using System.Collections.Generic;
//using System.Linq;

//namespace Lib_Core.Services.Helpers
//{
//    public class UserHelper
//    {
//        private IRepo<User> lora_Repo;
//        mdmsofd m = new mdmsofd();
//        public UserHelper(string lora_constr)
//        {
//            lora_Repo = new UserRepo(lora_constr);
//        }


//        public void CreateUsers()
//        {
//            List<emp_uuid> local_emps = m.emps.ToList<emp_uuid>();
//            List<string> lora_users = lora_Repo.Query.Select(u => u.Uuid).ToList<string>();
//            foreach (emp_uuid emp in local_emps)
//            {
//                if (local_emps.Where(e => e.OpusMedId.Equals(emp.OpusMedId)).Count() == 1)
//                {
//                    if (!lora_users.Contains(emp.orguuid))
//                    {
//                        User user = new User()
//                        {
//                            Opus_id = int.Parse(emp.OpusMedId),
//                            UserId = emp.samaccountname,
//                            Uuid = emp.orguuid,
//                            Phone = GetPhone(emp.OpusMedId),
//                            Email = GetMail(emp.OpusMedId),
//                            Updated = true
//                        };
//                        lora_Repo.Add(user);
//                    }
//                }
//            }
//        }

//        public void Mark_deleted_users()
//        {
//            List<string> mdm_ids = m.emps.Select(m => m.orguuid).ToList<string>();
//            foreach (User usr in lora_Repo.Query)
//            {
//                if (!mdm_ids.Contains(usr.Uuid))
//                {
//                    usr.Deleted_in_ad = true;
//                    lora_Repo.Update(usr);
//                }
//            }
//        }

//        private string GetPhone(string opus_id)
//        {
//            MedarbejderOplysninger res = m.meds.Where(m => m.OpusMedarbejderID == int.Parse(opus_id)).FirstOrDefault();
//            if (res != null)
//                return res.Tlfnr;
//            else
//                return null;
//        }

//        private string GetMail(string opus_id)
//        {
//            MedarbejderOplysninger res = m.meds.Where(m => m.OpusMedarbejderID == int.Parse(opus_id)).FirstOrDefault();
//            if (res != null)
//                return res.Mail;
//            else
//                return null;
//        }
//    }
//}
