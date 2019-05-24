using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using akubiz_lib;

namespace akubiz_app
{
    class Program
    {
        static void Main(string[] args)
        {
            EmployeeService es = new EmployeeService(Properties.Settings.Default.lora_constr);

        }
    }
}
