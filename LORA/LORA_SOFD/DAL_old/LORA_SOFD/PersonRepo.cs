using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class PersonRepo : IRepo<Person>
    {
        private LORA_SOFDDataContext c;
        private LogService log;
        public PersonRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
            log = new LogService(constr);
        }

        public IQueryable<Person> Query => c.Persons;

        public int Add(Person e)
        {
            c.Persons.InsertOnSubmit(e);
            c.SubmitChanges();
            log.Add_Log_entry("Added new Person. - Cpr: " + e.Cpr + " - system_id: " + e.System_id, "Person Created");
            return e.System_id;
        }

        public void Delete(Person e)
        {
            c.Persons.DeleteOnSubmit(e);
            c.SubmitChanges();
            log.Add_Log_entry("Deleted Person. - Cpr: " + e.Cpr + " - system_id: " + e.System_id, "Person Deleted");
        }

        public void Update(Person e)
        {
            c.SubmitChanges();
            log.Add_Log_entry("Updated Person. - Cpr: " + e.Cpr + " - system_id: " + e.System_id, "Person Updated");
        }
    }
}
