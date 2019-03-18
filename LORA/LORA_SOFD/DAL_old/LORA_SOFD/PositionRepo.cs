using System.Linq;

namespace DAL_old.LORA_SOFD
{
    public class PositionRepo : IRepo<Position>
    {
        private LORA_SOFDDataContext c;
        private LogService log;
        public PositionRepo(string constr)
        {
            c = new LORA_SOFDDataContext(constr);
            log = new LogService(constr);
        }

        public IQueryable<Position> Query => c.Positions;

        public int Add(Position e)
        {
            c.Positions.InsertOnSubmit(e);
            c.SubmitChanges();
            log.Add_Log_entry("Added new Position. - Opus: " + e.Opus_id + " - system_id: " + e.System_id, "Position Created");
            return e.System_id;
        }

        public void Delete(Position e)
        {
            c.Positions.DeleteOnSubmit(e);
            c.SubmitChanges();
            log.Add_Log_entry("Deleted Position. - Opus: " + e.Opus_id + " - system_id: " + e.System_id, "Position Deleted");
        }

        public void Update(Position e)
        {
            c.SubmitChanges();
            log.Add_Log_entry("Updated Position. - Opus: " + e.Opus_id + " - system_id: " + e.System_id, "Updated Deleted");
        }
    }
}
