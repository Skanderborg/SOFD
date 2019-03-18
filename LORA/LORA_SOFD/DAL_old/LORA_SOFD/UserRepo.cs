using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class UserRepo : IRepo<User>
    {
        private LORA_SOFDDataContext c;
        private LogService log;
        public UserRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
            log = new LogService(constr);
        }
        public IQueryable<User> Query => c.Users;

        public int Add(User e)
        {
            c.Users.InsertOnSubmit(e);
            c.SubmitChanges();
            log.Add_Log_entry("Added new User. - UserId: " + e.UserId + " - system_id: " + e.System_id, "User Created");
            return e.System_id;
        }

        public void Delete(User e)
        {
            c.Users.DeleteOnSubmit(e);
            c.SubmitChanges();
            log.Add_Log_entry("Deleted User. - UserId: " + e.UserId + " - system_id: " + e.System_id, "User Deleted");
        }

        public void Update(User e)
        {
            c.SubmitChanges();
            log.Add_Log_entry("Updated User. - UserId: " + e.UserId + " - system_id: " + e.System_id, "User Updated");
        }
    }
}
