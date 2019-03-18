using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class AdresseRepo : IRepo<Adress>
    {
        private LORA_SOFDDataContext context;
        private LogService log;
        public AdresseRepo(string constr)
        {
            context = new LORA_SOFDDataContext(constr);
            log = new LogService(constr);
        }
        public IQueryable<Adress> Query => context.Adresses;

        public int Add(Adress e)
        {
            context.Adresses.InsertOnSubmit(e);
            context.SubmitChanges();
            log.Add_Log_entry("Added new adress. - system_id: " + e.system_id, "Adr Created");
            return e.system_id;
        }

        public void Delete(Adress e)
        {
            context.Adresses.DeleteOnSubmit(e);
            context.SubmitChanges();
            log.Add_Log_entry("Deleted adress. - system_id: " + e.system_id, "Adr Deleted");
        }

        public void Update(Adress e)
        {
            context.SubmitChanges();
            log.Add_Log_entry("Updated adress. - system_id: " + e.system_id, "Adr Updated");
        }
    }
}
