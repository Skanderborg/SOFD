using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL_old
{
    public interface IRepoQueue<IEntity>
    {
        IQueryable<IEntity> Query { get; }
        long Add(IEntity e);
        void Delete(IEntity e);
        void Update(IEntity e);
    }
}
