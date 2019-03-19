using Lib_Core.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App_Console
{
    class Program
    {
        static void Main(string[] args)
        {
            // LORA SOFD
            LoraService ls = new LoraService(Properties.Settings.Default.smtpHost, Properties.Settings.Default.smtpPort, Properties.Settings.Default.smtpUser, Properties.Settings.Default.smtpPass,
                Properties.Settings.Default.smtpErrAdr, Properties.Settings.Default.dsa_sofd_constr, Properties.Settings.Default.lora_sofd_constr);
            bool lora_update = ls.Update(Properties.Settings.Default.differenceTolerence_org_vs_dsa);

            if (lora_update)
            {
                // STS kø
                QueueService qs = new QueueService(Properties.Settings.Default.lora_sofd_constr, Properties.Settings.Default.apikey, Properties.Settings.Default.cvr, Properties.Settings.Default.smtpHost,
                    Properties.Settings.Default.smtpPort, Properties.Settings.Default.smtpUser, Properties.Settings.Default.smtpPass, Properties.Settings.Default.smtpErrAdr);
                bool org_queue = qs.Complete_org_queue(Properties.Settings.Default.endpoint_orgunit);
                if (org_queue)
                {
                    qs.Complete_usr_queue(Properties.Settings.Default.endpoint_user);
                }
            }
        }
    }
}
