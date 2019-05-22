using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DAL_old;
using DAL_old.LORA_SOFD;

namespace akubiz_lib
{
    public class EmployeeService
    {
        IRepo<v_akubiz_employee> akubizRepo;

        public EmployeeService(string lora_constr)
        {
            akubizRepo = new AkubizRepo(lora_constr);
        }



    }
}
