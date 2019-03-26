using Lib_Core.Services.Emp;
using Lib_Core.Services.Org;
using System;
using Lib._365;

namespace Lib_Core.Services
{
    public class QueueService
    {
        private string lora_conStr;
        private string api_key;
        private string cvr;
        private EmailService email;
        private string mail_error;

        public QueueService(string lora_conStr, string api_key, string cvr, string smtp_host, int smpt_port, string smtp_user, string smtp_pass, string smtp_to_notify)
        {
            this.lora_conStr = lora_conStr;
            this.api_key = api_key;
            this.cvr = cvr;
            email = new EmailService(smtp_host, smpt_port, smtp_user, smtp_pass);
            mail_error = smtp_to_notify;
        }

        public bool Complete_org_queue(string end_orgunitspoint_url)
        {
            string current_fun = "Handle_creation()";
            try
            {
                OrgunitQueue org_queue = new OrgunitQueue(lora_conStr, api_key, end_orgunitspoint_url, cvr);
                org_queue.Handle_creation();
                current_fun = "Handle_updates()";
                org_queue.Handle_updates();
                current_fun = "Handle_Deletes()";
                org_queue.Handle_Deletes();
                return true;
            }
            catch (Exception e)
            {
                email.SendEmail(email.Get_Mailmessage(mail_error, "LORA_SOFD_ERROR", "Lib_Core.Services.QueueService.cs - Complete_org_queue() - kø funktion: " + current_fun + " - error message: " + e.Message));
                email.SendEmail(email.Get_Mailmessage("Mads.Nielsen@skanderborg.dk", "LORA_SOFD_ERROR", "Lib_Core.Services.QueueService.cs - Complete_org_queue() - kø funktion: " + current_fun + " - error message: " + e.Message));
                return false;
            }
        }

        /// <summary>
        /// OBS: Hvis en stilling både har en Updated og en Deleted i LORA_SOFD kø databasen for users, er brugere højest sandsynligt slettet, og derfor vil Updated fejle. Det burde aldrig ske,
        /// men det er sket et par gange i test-perioden fordi køen ikke blev behandlet hver dag og der typisk kommer en Updated dagen før en Deleted (muligvis fordi LØN sætter en slut-dato på).
        /// </summary>
        /// <param name="endpoint_users_url"></param>
        public bool Complete_usr_queue(string endpoint_users_url)
        {
            string current_fun = "Handle_creation()";
            try
            {
                UserQueue usr_queue = new UserQueue(lora_conStr, api_key, endpoint_users_url, cvr);
                usr_queue.Handle_creation();
                current_fun = "Handle_updates()";
                usr_queue.Handle_Updates();
                current_fun = "Handle_Deletes()";
                usr_queue.Handle_Deletes();
                return true;
            }
            catch (Exception e)
            {
                email.SendEmail(email.Get_Mailmessage(mail_error, "LORA_SOFD_ERROR", "Lib_Core.Services.QueueService.cs - Complete_usr_queue() - kø funktion: "+ current_fun + " - error message: " + e.Message));
                email.SendEmail(email.Get_Mailmessage("Mads.Nielsen@skanderborg.dk", "LORA_SOFD_ERROR", "Lib_Core.Services.QueueService.cs - Complete_usr_queue() - kø funktion: " + current_fun + " - error message: " + e.Message));
                return false;
            }
        }
    }
}
