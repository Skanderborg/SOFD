using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class OrgunitRepo : IRepo<Orgunit>
    {
        private LORA_SOFDDataContext context;
        private LogService log;
        public OrgunitRepo(string constr)
        {
            context = new LORA_SOFDDataContext(constr);
            log = new LogService(constr);
        }
        public IQueryable<Orgunit> Query => context.Orgunits;

        public int Add(Orgunit e)
        {
            context.Orgunits.InsertOnSubmit(e);
            context.SubmitChanges();
            log.Add_Log_entry("Added new orgunit. - LongName: " + e.Name + " - LosID: " + e.Los_id + " - system_id: " + e.System_id, "Org Created");
            return e.System_id;
        }

        public void Delete(Orgunit e)
        {
            context.Orgunits.DeleteOnSubmit(e);
            context.SubmitChanges();
            log.Add_Log_entry("Deleted new orgunit. - LongName: " + e.Name + " - LosID: " + e.Los_id + " - system_id: " + e.System_id, "Org Deleted");
        }

        public void Update(Orgunit e)
        {
            context.SubmitChanges();
            log.Add_Log_entry("Updated new orgunit. - LongName: " + e.Name + " - LosID: " + e.Los_id + " - system_id: " + e.System_id, "Org Updated");
        }
    }
}
