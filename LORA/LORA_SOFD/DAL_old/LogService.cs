using System;
using DAL_old.LORA_SOFD;

namespace DAL_old
{
    public class LogService
    {
        private IRepo<change> changeRepo;

        public LogService(string constr)
        {
            changeRepo = new ChangeRepo(constr);
        }

        public void Add_Log_entry(string changed_text, string action)
        {
            changeRepo.Add(new change()
            {
                action = action,
                change_text = changed_text,
                change_date = DateTime.Now
            });
        }
    }
}
