using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace acubiz_lib.Models
{
    internal class Acubiz_Emp
    {
        internal string uuid { get; set; }
        internal string fullname { get; set; }
        internal string ad1 { get; set; }
        internal string ad2 { get; set; }
        internal string ad3 { get; set; }
        internal string manager_uuid { get; set; }
        internal string email { get; set; }
        internal string cost_center { get; set; } // skal være blank
        internal string los_id1 { get; set; }
        internal string los_id2 { get; set; } // los_id + los longname
        internal string cpr1 { get; set; }
        internal string cpr2 { get; set; }
        internal string nul { get; set; }
    }
}
