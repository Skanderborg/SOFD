using System;
using Lib._365;
using OS2Rollekatalog.Service;

namespace OS2Rollekatalog
{
    class Program
    {
        static void Main(string[] args)
        {
            EmailService email = new EmailService(Properties.Settings.Default.smtpHost, Properties.Settings.Default.smtpPort, Properties.Settings.Default.smtpUser, Properties.Settings.Default.smtpPass);
            try
            {
                JsonService js = new JsonService(Properties.Settings.Default.lora_sofd_constr, Properties.Settings.Default.parentOrgID);
                js.PostJson(Properties.Settings.Default.apiKey, Properties.Settings.Default.endPointUrl);
            }
            catch (Exception e)
            {
                email.SendEmail(email.Get_Mailmessage(Properties.Settings.Default.smtpErrAdr, "LORA_SOFD_OS2ROLLEKATALOG ERROR", "error message: " + e.Message));
                email.SendEmail(email.Get_Mailmessage("dof@skanderborg.dk", "LORA_SOFD_OS2ROLLEKATALOG ERROR", "error message: " + e.Message));
            }
        }
    }
}
