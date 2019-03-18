using DAL_old;
using DAL_old.LORA_SOFD;
using System.Linq;

namespace Lib_Core.Services
{
    internal class AdressService
    {
        private IRepo<Adress> adresseRepo;

        internal AdressService(string lora_constr)
        {
            adresseRepo = new AdresseRepo(lora_constr);
        }

        /// <summary>
        /// Henter reference til system_id på en eksisterende adresse, hvis der er en, ellers oprettes en ny.
        /// </summary>
        /// <param name="adr_gade"></param>
        /// <param name="adr_postnr"></param>
        /// <param name="adr_by"></param>
        /// <returns>system_id for dbo.adresses</returns>
        internal int Get_Adress_id(string adr_gade, int? adr_postnr, string adr_by)
        {
            if (adr_gade == null)
            {
                adr_gade = "Mangler, spørg løn";
                adr_by = "Mangler, spørg løn";
            }

            if (adr_gade.Contains("ADRESSEBESKYTTET"))
            {
                adr_gade = "**ADRESSEBESKYTTET**";
                adr_by = "**ADRESSEBESKYTTET**";
            }

            if (adr_by == null)
            {
                adr_gade = "Mangler, spørg løn";
                adr_by = "Mangler, spørg løn";
            }

            Adress adr = adresseRepo.Query.Where(a => a.gade.Equals(adr_gade) && a.postnr == adr_postnr && a.by.Equals(adr_by)).FirstOrDefault();
            if (adr == null)
            {
                return adresseRepo.Add(new Adress()
                {
                    gade = adr_gade,
                    postnr = (int)adr_postnr,
                    by = adr_by
                });
            }
            else
            {
                return adr.system_id;
            }
        }

        internal void Delete_Adr(int adr_id)
        {
            Adress adr = adresseRepo.Query.Where(a => a.system_id == adr_id).FirstOrDefault();
            if(adr != null)
                adresseRepo.Delete(adr);
        }
    }
}
