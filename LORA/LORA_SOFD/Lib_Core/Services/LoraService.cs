using System;
using System.Collections.Generic;
using DAL_old;
using Lib._365;
using Lib_Core.Services.Emp;
using Lib_Core.Services.Helpers;
using Lib_Core.Services.Org;

namespace Lib_Core.Services
{
    public class LoraService
    {
        private EmailService email;
        private string mail_error;
        private LogService log;
        string smtp_to_notify;
        private OrgunitService orgService;
        private PositionService positionService;
        string lora_constr;
        private string last_step = "";
        private ManagerSetupHelper managerSetupHelper;

        public LoraService(string smtp_host, int smpt_port, string smtp_user, string smtp_pass, string smtp_to_notify, string dsa_constr, string lora_constr)
        {
            email = new EmailService(smtp_host, smpt_port, smtp_user, smtp_pass);
            log = new LogService(lora_constr);
            this.smtp_to_notify = smtp_to_notify;
            orgService = new OrgunitService(dsa_constr, lora_constr);
            positionService = new PositionService(lora_constr, dsa_constr);
            mail_error = smtp_to_notify;
            this.lora_constr = lora_constr;
            managerSetupHelper = new ManagerSetupHelper(lora_constr);
        }

        public bool Update(int difference_tolerance_orgunits)
        {
            // hvis forskellen på DSA sofd og LORA sofd er mindre end tolerancen, kører processen, ellers bliver adm advaret - dette er sat op fordi KMD nogen gange fucker op
            if(orgService.Get_DSA_LORA_ORG_difference() < difference_tolerance_orgunits)
            {
                Update_Lora();
                return true;
                try
                {
                    Update_Lora();
                    return true;
                }
                catch (Exception e)
                {
                    email.SendEmail(email.Get_Mailmessage(mail_error, "LORA_SOFD_ERROR", "Lib_Core.Services.LoraService.cs - Update() - problem i indre Update_Lora() - last_step = " + last_step + " - error message: " + e.Message));
                    //email.SendEmail(email.Get_Mailmessage("Mads.Nielsen@skanderborg.dk", "LORA_SOFD_ERROR", "LoraService.cs - Update() - problem i indre Update_Lora() - last_step = " + last_step + " - error message: " + e.Message));
                    //email.SendEmail(email.Get_Mailmessage("dof@skanderborg.dk", "LORA_SOFD_ERROR", "LoraService.cs - Update() - problem i indre Update_Lora() - last_step = " + last_step + " - error message: " + e.Message));
                    return false;
                }
            }
            else
            {
                email.SendEmail(email.Get_Mailmessage(mail_error, "LORA_SOFD_ERROR", "Lib_Core.Services.LoraService.cs - Update() - Der er for stor forskel på antallet af orgunits i DSA_SOFD og " +
                    "LORA_SOFD databaserne i forhold til difference_tolerance_orgunits variablen, hvis der ikke har været store Organisationsændringer er det sandsynligt, at KMD -> DSA_SOFD " +
                    "på ssis er gået galt"));
                email.SendEmail(email.Get_Mailmessage("Mads.Nielsen@skanderborg.dk", "LORA_SOFD_ERROR", "Lib_Core.Services.LoraService.cs - Update() - Der er for stor forskel på antallet af orgunits i DSA_SOFD og " +
                    "LORA_SOFD databaserne i forhold til difference_tolerance_orgunits variablen, hvis der ikke har været store Organisationsændringer er det sandsynligt, at KMD -> DSA_SOFD " +
                    "på ssis er gået galt"));
                email.SendEmail(email.Get_Mailmessage("dof@skanderborg.dk", "LORA_SOFD_ERROR", "Lib_Core.Services.LoraService.cs - Update() - Der er for stor forskel på antallet af orgunits i DSA_SOFD og " +
                    "LORA_SOFD databaserne i forhold til difference_tolerance_orgunits variablen, hvis der ikke har været store Organisationsændringer er det sandsynligt, at KMD -> DSA_SOFD " +
                    "på ssis er gået galt"));
                return false;
            }
        }

        private void Update_Lora()
        {
            last_step = "Update_Lora()";
            // Tilføjer nye Organisations enheder til LORA_SOFD
            orgService.Add_new_Orgunits();
            last_step = "orgService.Add_new_Orgunits();";

            // Tilknytter UUID til de nye Organisations enehder
            // Opretter Created events i STS org køen
            // OBS: Skal afskaffes når AD ikke længere står for UUIDs til orgunits:
            orgService.Add_UUIDs_to_Orgunits();
            last_step = "orgService.Add_UUIDs_to_Orgunits();";

            // Opdaterer de organisatoriske forandringer, der har været i OPUS inden for de seneste 5 dage i LORA_SOFD
            // Opretter Updated events i STS org køen
            // OBS: de 5 dage kan nok forbedres.
            orgService.Update_Orgunits();
            last_step = "orgService.Update_Orgunits();";

            List<int> lora_org_ids = orgService.Get_lora_org_ids();

            // Tilføjer nye ansættelser til LORA_SOFD
            positionService.Add_new_positions(lora_org_ids);
            last_step = "positionService.Add_new_positions(lora_org_ids);";

            // Opdaterer de ansættelsesmæssige forandringer, der har været i OPUS inden for de seneste 5 dage i LORA_SOFD
            // Opretter Updated events i STS user køen
            // Opretter Updated events i AD user køen
            // OBS: de 5 dage kan nok forbedres.
            positionService.Update_positions_from_dsa(lora_org_ids); // null persons?
            last_step = "positionService.Update_positions(lora_org_ids);";

            // Opdaterer forandringer fra AD
            positionService.Add_updated_users_to_sts_org();
            last_step = "positionService.Add_updated_users_to_sts_org()";

            // Fjerner de AD brugere som er markerede som slettede i LORA_SOFDs user tabel.
            // Opretter Deleted events i STS user køen
            // Sletter fra User tabellen
            positionService.Delete_deleted_users();
            last_step = "positionService.Delete_deleted_users();";

            // Finder de ansættelser som ikke længere eksisterer
            // Opretter Deleted events i STS user køen
            // Sletter fra Positions, Adresses og Persons tabellerne
            positionService.Delete_deleted_positions();
            last_step = "positionService.Delete_deleted_positions();";

            // Gennemgår listen af LORA_SOFD.Positions som endnu ikke har tilknyttet en USER, laver et tjek på om der er en ny LORA_SOFD.User tilknyttet til medarbejdernummeret
            // Opretter Created events i STS user køen
            positionService.Add_new_users_to_positions();
            last_step = "positionService.Add_new_users_to_positions();";

            // Finder de organisatoriske enheder som ikke længere eksisterer
            // Opretter Deleted events i STS org køen
            orgService.Delete_Orgunits();
            last_step = "orgService.Delete_Orgunits();";

            // opdaterer tabellen over employees og deres ledere
            managerSetupHelper.Handle_Manager_Lookups();
            last_step = "handle_manager_lookups()";
        }
    }
}
