using DAL_old;
using DAL_old.DSA_SOFD;
using DAL_old.LORA_SOFD;
using DAL_old.LORA_SOFD_QUEUE;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Lib_Core.Services.Org
{
    internal class OrgunitService
    {
        private IRepo<OrgUnit> dsa_orgRepo;
        private IRepo<org_uiid> org_uuid_repo;
        private AdressService adr_service;
        private IRepo<Orgunit> lora_orgRepo;
        private IQueryable<OrgUnit> dsa_orgs;
        private List<int> dsa_ids;
        private OrgunitQueue queue;
        private IRepo<ad_org_action> ad_org_change_repo;

        internal OrgunitService(string dsa_constr, string lora_constr)
        {
            dsa_orgRepo = new OrgUnitRepo(dsa_constr);
            lora_orgRepo = new OrgunitRepo(lora_constr);
            adr_service = new AdressService(lora_constr);
            org_uuid_repo = new Org_uuid_repo(lora_constr);
            dsa_orgs = Get_dsa_orgs(); // OBS skal før dsa_ids
            dsa_ids = Get_dsa_orgids();
            queue = new OrgunitQueue(lora_constr);
            ad_org_change_repo = new Ad_org_change_repo(lora_constr);
        }

        #region setup
        /// <summary>
        /// Henter de relevante LOS enheder fra DSA SOFD, der bliver pillet en række fra fordi forretningen har valgt de ikke skal med.
        /// 
        /// LOS ID på de som er pillet fra:
        /// 855822 - Tabt arbejdsfortj.
        /// 871163 - Handicaphjælper
        /// 878672 - Handicaphjælpere - børn og unge
        /// 878771 - Aflastningsfamilie
        /// 878772 - Plejefamilie
        /// 878773 - Kontaktperson
        /// 878774 - Lommepenge
        /// 878775 - Støtteperson
        /// 878776 - Personlige rådgivere
        /// 878777 - Ledsagerordning
        /// 878778 - Formidling praktikophold'
        /// 871164 - Ledsager
        /// 871165 - Plejer og aflastning
        /// 878201 - Folkeoplysningsområdet
        /// 833528 - å historik
        /// 
        /// LOS enheder med # i navnet, er der for historiske årsager, og er ikke aktive
        /// </summary>
        private IQueryable<OrgUnit> Get_dsa_orgs()
        {
            return dsa_orgRepo.Query.Where(dao => dao.longName.Contains("#") == false && dao.id != 855822 && dao.id != 871163 && dao.id != 878672 && dao.id != 878771
                        && dao.id != 878772 && dao.id != 878773 && dao.id != 878774 && dao.id != 878775 && dao.id != 878776 && dao.id != 878777 && dao.id != 878778 && dao.id != 871164
                        && dao.id != 871165 && dao.id != 878201 && dao.id != 833528);
        }

        private List<int> Get_dsa_orgids()
        {
            List<int> res = new List<int>();
            foreach(OrgUnit org in dsa_orgs)
            {
                res.Add(org.id ?? 0);
            }
            return res;
        }
        #endregion

        /// <summary>
        /// Beregner forskellen mellem antallet af Orgunits i det indkomne data-sæt og LORA, kan bruges til at sætte en tolerance for forskellen.
        /// Hvis forskellen er for stor, er det muligt, at der er problemer med KMD udtrækket som DSA indlæser næsten ukritisk.
        /// </summary>
        /// <returns></returns>
        internal int Get_DSA_LORA_ORG_difference()
        {
            int currentLoraOrgs = lora_orgRepo.Query.Count();
            int dsaOrgs = dsa_orgRepo.Query.Where(dsao => dsao.longName.Contains("#") == false).Count();
            return currentLoraOrgs - dsaOrgs;
        }

        /// <summary>
        /// Henter org units fra DSA sofd, og tjekker om de eksiterer i lora sofd, hvis de ikke gør det, oprettes en ny Orgunit i LORA SOFD
        /// 
        /// OBS, når vi overtager UUID creation for organisations UUID'er, skal de tilføjes til STS køen her - dette er kodet, men er deaktiveret
        /// </summary>
        internal void Add_new_Orgunits()
        {
            List<int> lora_org_ids = lora_orgRepo.Query.Select(o => o.Los_id).ToList();
            foreach (OrgUnit dsaorg in dsa_orgs.OrderBy(o => o.OrgNveau))
            {
                if (!lora_org_ids.Contains(dsaorg.id ?? 0))
                {
                    int parent_id = Get_parent_los_id(dsaorg.parentOrgUnit);
                    int los_id = dsaorg.id ?? 0;
                    int adresse_ref = adr_service.Get_Adress_id(dsaorg.street, (int)dsaorg.zipCode, dsaorg.city);
                    Orgunit org = UpdateOrgunit(new Orgunit(), true, "", los_id, dsaorg.longName, "", (DateTime)dsaorg.startDate, Get_phone(), Get_email(), parent_id, dsaorg.shortName,
                            adresse_ref, dsaorg.eanNr, dsaorg.pNr, dsaorg.costCenter, dsaorg.orgTypeTxt, (int)dsaorg.OrgNveau);

                    lora_orgRepo.Add(org);
                    // queue.Add_Org_queue_item(org.Uuid, org.Los_id, "Created"); <- skal først aktiveres når LORA SOFD skriver UUID indtil da se: Add_UUIDs_to_Orgunits()

                    // fortæller AD at der er en ny org unit
                    ad_org_change_repo.Add(new ad_org_action() {
                        uuid = null,
                        los_id = org.Los_id,
                        action = "created"
                    });
                }
            }
        }

        /// <summary>
        /// Henter de org units, som har ændret sig inden for de seneste 5 dage og opdatere dem, hvis der er forandringer. Det er lidt åndsvagt at en enhed bliver tjekket 5 gange,
        /// men det er konsekvensen af full load i DSA sofd.
        /// 
        /// Hvis der er forandringer, skal disses sendes til STS.
        /// 
        /// OBS de 5 dage kan højest sandsynligt sættes ned til 3, men DSA udtrækket kører ikke hver dag, så for en sikkerhedsskyld starter vi på 5.
        /// </summary>
        internal void Update_Orgunits()
        {
            List<int> lora_org_ids = lora_orgRepo.Query.Select(o => o.Los_id).ToList();
            foreach (OrgUnit dsaorg in dsa_orgs)//.Where(da => da.lastChanged > DateTime.Now.AddDays(-5)))
            {
                if (lora_org_ids.Contains((int)dsaorg.id))
                {
                    int parent_id = Get_parent_los_id(dsaorg.parentOrgUnit);

                    int los_id = (int)dsaorg.id;
                    int adresse_ref = adr_service.Get_Adress_id(dsaorg.street, (int)dsaorg.zipCode, dsaorg.city);
                    Orgunit _lora = lora_orgRepo.Query.Where(o => o.Los_id == los_id).First();

                    if (!dsaorg.longName.Equals(_lora.Name) || parent_id != _lora.Parent_losid || dsaorg.eanNr != _lora.Ean || dsaorg.pNr != _lora.Pnr || dsaorg.costCenter != _lora.Cost_center
                        || !dsaorg.orgTypeTxt.Equals(_lora.Org_type) || (int)dsaorg.OrgNveau != _lora.Org_niveau || adresse_ref != _lora.Adress_ref)
                    {
                        Orgunit org = UpdateOrgunit(_lora, false, "", los_id, dsaorg.longName, "", (DateTime)dsaorg.startDate, Get_phone(), Get_email(), parent_id, dsaorg.shortName,
                            adresse_ref, dsaorg.eanNr, dsaorg.pNr, dsaorg.costCenter, dsaorg.orgTypeTxt, (int)dsaorg.OrgNveau);

                        lora_orgRepo.Update(org);
                        queue.Add_Org_queue_item(org.Uuid, org.Los_id, org.Org_niveau, "Updated");

                        // fortæller AD at der er slettet en org
                        ad_org_change_repo.Add(new ad_org_action()
                        {
                            uuid = org.Uuid,
                            los_id = org.Los_id,
                            action = "updated"
                        });
                    }
                }
            }
        }

        /// <summary>
        /// Finder de organisatoriske enheder som ikke længere eksisterer, og markerer dem til sletning i STS køen.
        /// </summary>
        internal void Delete_Orgunits()
        {
            List<int> lora_org_ids = lora_orgRepo.Query.Select(o => o.Los_id).ToList();
            foreach (int lora_los_id in lora_org_ids)
            {
                if (!dsa_ids.Contains(lora_los_id))
                {
                    Orgunit org = lora_orgRepo.Query.Where(o => o.Los_id == lora_los_id).First();
                    queue.Add_Org_queue_item(org.Uuid, lora_los_id, org.Org_niveau, "Deleted");

                    // fortæller AD at der er slettet en org
                    ad_org_change_repo.Add(new ad_org_action()
                    {
                        uuid = org.Uuid,
                        los_id = org.Los_id,
                        action = "deleted"
                    });

                    lora_orgRepo.Delete(org);
                }
            }
        }

        internal List<int> Get_lora_org_ids()
        {
            return lora_orgRepo.Query.Select(o => o.Los_id).ToList();
        }

        private string Get_phone()
        {
            return "87947000";
        }

        private string Get_email()
        {
            return "skanderborg.kommune@skanderborg.dk";
        }

        private int Get_parent_los_id(string id)
        {
            int parent_id;

            if (int.TryParse(id, out parent_id))
                return parent_id;
            else
                return 0;
        }

        private Orgunit UpdateOrgunit(Orgunit org, bool is_new_org, string uuid, int los_id, string name, string payoutUnitUuid, DateTime created_date, string phone,
            string email, int parent_losid, string los_short_name, int adress_ref, Int64? ean, Int64? pnr, Int64? cost_center, string org_type, int org_niveau)
        {
            // los_id er unique i DB
            if (is_new_org)
            {
                org.Uuid = uuid;
                org.Los_id = los_id;
            }
            org.Name = name;
            org.PayoutUnitUuid = payoutUnitUuid;
            org.Created_date = created_date;
            org.Phone = phone;
            org.Email = email;
            org.Parent_losid = parent_losid;
            org.Los_short_name = los_short_name;
            org.Adress_ref = adress_ref;
            org.Last_changed = DateTime.Now;
            org.Ean = ean;
            org.Pnr = pnr;
            org.Cost_center = cost_center;
            org.Org_type = org_type;
            org.Org_niveau = org_niveau;
            return org;
        }

        /// <summary>
        /// Tilknytter UUID'er til nye organisations enehder og tilføjer dem til STS køen.
        /// 
        /// OBS dette skal afskaffes når vi tager ejerskab over org UUID'er
        /// </summary>
        internal void Add_UUIDs_to_Orgunits()
        {
            //MDMSOFD.mdmsofd mdm = new MDMSOFD.mdmsofd();
            foreach (Orgunit org in lora_orgRepo.Query.Where(o => o.Uuid.Length < 1))
            {
                org_uiid morg = org_uuid_repo.Query.Where(o => o.OrgOpusID.Equals(org.Los_id.ToString())).FirstOrDefault();
                if(morg != null && morg.orguuid != null && morg.orguuid.Length > 5)
                {
                    org.Uuid = morg.orguuid;
                    lora_orgRepo.Update(org);
                    queue.Add_Org_queue_item(org.Uuid, org.Los_id, org.Org_niveau, "Created");
                }
            }
        }
    }
}












        