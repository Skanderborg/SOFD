﻿using System;
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

        public LoraService(string smtp_host, int smpt_port, string smtp_user, string smtp_pass, string smtp_to_notify, string dsa_constr, string lora_constr)
        {
            email = new EmailService(smtp_host, smpt_port, smtp_user, smtp_pass);
            log = new LogService(lora_constr);
            this.smtp_to_notify = smtp_to_notify;
            orgService = new OrgunitService(dsa_constr, lora_constr);
            positionService = new PositionService(lora_constr, dsa_constr);
            mail_error = smtp_to_notify;
            this.lora_constr = lora_constr;
        }

        public void Update(int difference_tolerance_orgunits)
        {
            // hvis forskellen på DSA sofd og LORA sofd er mindre end tolerancen, kører processen, ellers bliver adm advaret - dette er sat op fordi KMD nogen gange fucker op
            if(orgService.Get_DSA_LORA_ORG_difference() < difference_tolerance_orgunits)
            {
                //Update_Lora();
                try
                {
                    Update_Lora();
                }
                catch(Exception e)
                {
                    email.SendEmail(email.Get_Mailmessage(mail_error, "LORA_SOFD_ERROR", "Lib_Core.Services.LoraService.cs - Update() - problem i indre Update_Lora() kald - error message: " + e.Message));
                    email.SendEmail(email.Get_Mailmessage("Mads.Nielsen@skanderborg.dk", "LORA_SOFD_ERROR", "LoraService.cs - Update() - problem i indre Update_Lora() kald - error message: " + e.Message));
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
            }
        }

        private void Update_Lora()
        {
            // Tilføjer nye Organisations enheder til LORA_SOFD
            orgService.Add_new_Orgunits();

            // Tilknytter UUID til de nye Organisations enehder
            // Opretter Created events i STS org køen
            // OBS: Skal afskaffes når AD ikke længere står for UUIDs til orgunits:
            orgService.Add_UUIDs_to_Orgunits();

            // Opdaterer de organisatoriske forandringer, der har været i OPUS inden for de seneste 5 dage i LORA_SOFD
            // Opretter Updated events i STS org køen
            // OBS: de 5 dage kan nok forbedres.
            orgService.Update_Orgunits();

            List<int> lora_org_ids = orgService.Get_lora_org_ids();

            // Tilføjer nye ansættelser til LORA_SOFD
            positionService.Add_new_positions(lora_org_ids);

            // Opdaterer de ansættelsesmæssige forandringer, der har været i OPUS inden for de seneste 5 dage i LORA_SOFD
            // Opretter Updated events i STS user køen
            // Opretter Updated events i AD user køen
            // OBS: de 5 dage kan nok forbedres.
            positionService.Update_positions(lora_org_ids); // null persons?

            // Opdaterer users - positions - opdateringer fra ad tror jeg OBS IKKE DONE
            string s = "";

            // Benytter UserHelper servicen til at opdaterer nye og slettede AD brugere i LORA_SOFDs user tabel
            // OBS: Dette er en midlertidig løsning, som skal erstattes af AD oprettelses flowet + AD event scripts på opdateringer og deaktiveringer
            UserHelper userHelper = new UserHelper(lora_constr);
            userHelper.CreateUsers();
            userHelper.Mark_deleted_users();

            // Fjerner de AD brugere som er markerede som slettede i LORA_SOFDs user tabel.
            // Opretter Deleted events i STS user køen
            // Sletter fra User tabellen
            positionService.Delete_deleted_users();

            // Finder de ansættelser som ikke længere eksisterer
            // Opretter Deleted events i STS user køen
            // Sletter fra Positions, Adresses og Persons tabellerne
            positionService.Delete_deleted_positions();

            // Gennemgår listen af LORA_SOFD.Positions som endnu ikke har tilknyttet en USER, laver et tjek på om der er en ny LORA_SOFD.User tilknyttet til medarbejdernummeret
            // Opretter Created events i STS user køen
            positionService.Add_new_users_to_positions();

            // Finder de organisatoriske enheder som ikke længere eksisterer
            // Opretter Deleted events i STS org køen
            orgService.Delete_Orgunits();
        }
    }
}