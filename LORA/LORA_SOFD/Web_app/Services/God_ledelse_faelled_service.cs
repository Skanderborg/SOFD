using DAL_old;
using DAL_old.LORA_SOFD_SERVICE;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Web_app.Services
{
    public class God_ledelse_faelled_service
    {
        private IRepo<god_ledelse_pnr> pnrRepo;
        private IRepo<v_god_ledelse_fælleden> glfRepo;

        public God_ledelse_faelled_service()
        {
            pnrRepo = new God_ledelse_pnrRepo(Properties.Settings.Default.lora_sofd_constr);
            glfRepo = new God_ledelse_faelledRepo(Properties.Settings.Default.lora_sofd_constr);
        }




    }
}