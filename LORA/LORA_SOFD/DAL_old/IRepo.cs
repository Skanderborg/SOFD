using System.Linq;

namespace DAL_old
{
    public interface IRepo<IEntity>
    {
        IQueryable<IEntity> Query { get; }
        int Add(IEntity e);
        void Delete(IEntity e);
        void Update(IEntity e);
    }
}
