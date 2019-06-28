using DAL_old;
using DAL_old.DSA_SOFD;
using DAL_old.LORA_SOFD;
using DAL_old.LORA_SOFD_QUEUE;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Lib_Core.Services.Emp
{
    internal class PositionService
    {
        private IRepo<Position> posRepo;
        private IRepo<User> useRepo;
        private IRepo<Person> perRepo;
        private IRepoQueue<qUser> queue_user;
        private IRepo<ad_user_org_change> ad_user_org_change_repo;
        private AdressService adr;
        private IRepo<v_emp> dsa_emp_repo;
        IQueryable<v_emp> dsa_emps;
        private List<int> dsa_ids;

        internal PositionService(string lora_constr, string dsa_constr)
        {
            posRepo = new PositionRepo(lora_constr);
            useRepo = new UserRepo(lora_constr);
            perRepo = new PersonRepo(lora_constr);
            queue_user = new QUserRepo(lora_constr);
            ad_user_org_change_repo = new Ad_user_org_change_repo(lora_constr);
            adr = new AdressService(lora_constr);
            dsa_emp_repo = new EmployeeRepo(dsa_constr);
            dsa_emps = Get_dsa_emps(); //obs skal køres først
            Set_dsa_ids();
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
        private IQueryable<v_emp> Get_dsa_emps()
        {
            return dsa_emp_repo.Query.Where(e => !(e.entryDate == null && e.initialEntry == null) && e.orgUnit != 855822 && e.orgUnit != 871163 && e.orgUnit != 878672 &&
             e.orgUnit != 878771 && e.orgUnit != 878772 && e.orgUnit != 878773 && e.orgUnit != 878774 && e.orgUnit != 878775 && e.orgUnit != 878776 && e.orgUnit != 878777 &&
             e.orgUnit != 878778 && e.orgUnit != 871164 && e.orgUnit != 871165 && e.orgUnit != 878201 && e.orgUnit != 833528 && e.firstName != null);
        }

        private void Set_dsa_ids()
        {
            dsa_ids = new List<int>();
            foreach(v_emp e in dsa_emps)
            {
                dsa_ids.Add((int)e.opus_medid);
            }
        }
        #endregion

        internal void Add_new_positions(List<int> lora_los_ids)
        {
            List<int> lora_opus_ids = posRepo.Query.Select(p => p.Opus_id).ToList();
            foreach (v_emp emp in dsa_emps)
            {
                int emp_opus_id = (int)emp.opus_medid;
                int emp_los_id = (int)emp.orgUnit;
                // er det en ny position
                if (!lora_opus_ids.Contains(emp_opus_id))
                {
                    // kan kun tilføjes hvis medarbejders org er i lora_sofd
                    if (lora_los_ids.Contains(emp_los_id))
                    {
                        DateTime ans_dato;
                        if (emp.entryDate != null)
                            ans_dato = DateTime.ParseExact(emp.entryDate, "yyyy-MM-dd", null);
                        else
                            ans_dato = DateTime.ParseExact(emp.initialEntry, "yyyy-MM-dd", null);

                        DateTime? fra_dato = null;
                        if (emp.leaveDate != null)
                            fra_dato = DateTime.ParseExact(emp.leaveDate, "yyyy-MM-dd", null);

                        int postal;
                        int.TryParse(emp.postalCode, out postal);

                        int privat_adr_id = adr.Get_Adress_id(emp.adress, postal, emp.city);
                        Person per = Get_Person(emp.cprnr, emp.firstName, emp.lastName, privat_adr_id);
                        Position pos = Get_Position(new Position(), true, emp_opus_id, emp.position, emp_los_id, emp.cprnr, ans_dato, fra_dato, (bool)emp.isManager, (decimal)emp.numerator,
                            int.Parse(emp.workContract), emp.workContractText);
                        posRepo.Add(pos);
                    }
                    else
                    {
                        throw new Exception("Medarbejder med opus id: " + emp.opus_medid + " er i org med los id: " + emp.orgUnit + " som ikke findes i lora_sofd");
                    }
                }
            }
        }

        internal void Update_positions_from_dsa(List<int> lora_los_ids)
        {
            List<int> lora_opus_ids = posRepo.Query.Select(p => p.Opus_id).ToList();
            foreach (v_emp emp in dsa_emps)//.Where(e => e.lastChanged > DateTime.Now.AddDays(-5)))
            {
                int emp_opus_id = (int)emp.opus_medid;
                int emp_los_id = (int)emp.orgUnit;
                if (lora_los_ids.Contains(emp_los_id))
                {
                    Position pos = posRepo.Query.Where(p => p.Opus_id == emp_opus_id).FirstOrDefault();
                    if (pos == null)
                        throw new Exception("Forsøgte at opdaterer en ikke eksisterende lora position for dsa_opus_id: " + emp_opus_id);

                    DateTime ans_dato;
                    if (emp.entryDate != null)
                        ans_dato = DateTime.ParseExact(emp.entryDate, "yyyy-MM-dd", null);
                    else
                        ans_dato = DateTime.ParseExact(emp.initialEntry, "yyyy-MM-dd", null);

                    DateTime? fra_dato = null;
                    if (emp.leaveDate != null)
                        fra_dato = DateTime.ParseExact(emp.leaveDate, "yyyy-MM-dd", null);

                    int postal;
                    int.TryParse(emp.postalCode, out postal);
                    int old_adr_fk = pos.Person.Private_adr_fk;
                    int privat_adr_id = adr.Get_Adress_id(emp.adress, postal, emp.city);
                    string _firstname = pos.Person.Firstname;
                    string _lastname = pos.Person.Lastname;

                    bool updates = false;
                    bool has_org_unit_changed = false;
                    // har Person ændret sig
                    if(!emp.firstName.Equals(_firstname) || !emp.lastName.Equals(_lastname) || old_adr_fk != privat_adr_id)
                    {
                        Get_Person(pos.Person_fk, emp.firstName, emp.lastName, privat_adr_id);
                        updates = true;
                    }
                    // har position ændret sig
                    if (pos.Name != emp.position || pos.Orgunit_losid_fk != emp_los_id || pos.Ans_dato != ans_dato || pos.Fra_dato != fra_dato || pos.Is_Manager != (bool)emp.isManager ||
                            pos.Timetal != emp.numerator || pos.Pay_method != int.Parse(emp.workContract) || pos.Pay_method_text != emp.workContractText)
                    {
                        if (pos.Orgunit_losid_fk != emp_los_id)
                        {
                            has_org_unit_changed = true;
                        }
                        pos = Get_Position(pos, false, emp_opus_id, emp.position, emp_los_id, emp.cprnr, ans_dato, fra_dato, (bool)emp.isManager, (decimal)emp.numerator,
                        int.Parse(emp.workContract), emp.workContractText);
                        updates = true;
                    }

                    // hvis de rer ændringer skal user muligvis opdateres i STS og i AD
                    if (updates)
                    {
                        posRepo.Update(pos);
                        if (pos.User != null)
                        {
                            queue_user.Add(new qUser()
                            {
                                Opus_id = pos.Opus_id,
                                Change_type = "Updated",
                                Time_added = DateTime.Now,
                                Uuid = pos.User.Uuid
                            });

                            if (has_org_unit_changed)
                            {
                                ad_user_org_change_repo.Add(new ad_user_org_change()
                                {
                                    Uuid = pos.User_fk,
                                    Orgunit_los_id = pos.Orgunit_losid_fk,
                                    action = "updated",
                                });
                            }
                        }
                    }
                }
                else
                {
                    throw new Exception("Medarbejder med opus id: " + emp.opus_medid + " er i org med los id: " + emp.orgUnit + " som ikke findes i lora_sofd");
                }
            }
        }

        internal void Delete_deleted_positions()
        {
            List<int> lora_opus_ids = posRepo.Query.Select(p => p.Opus_id).ToList();
            foreach (int lora_id in lora_opus_ids)
            {
                if (!dsa_ids.Contains(lora_id))
                {
                    
                    Position pos = posRepo.Query.Where(p => p.Opus_id == lora_id).First();
                    string cpr = pos.Person_fk;
                    int adr_id = pos.Person.Private_adr_fk;
                    // har user?
                    if (pos.User != null)
                    {
                        qUser usr = new qUser()
                        {
                            Change_type = "Deleted",
                            Opus_id = pos.Opus_id,
                            Time_added = DateTime.Now,
                            Uuid = pos.User.Uuid
                        };
                        queue_user.Add(usr);
                        pos.User = null;
                        posRepo.Update(pos);
                        pos = posRepo.Query.Where(p => p.Opus_id == lora_id).First();
                    }

                    posRepo.Delete(pos);

                    // er person i brug?
                    if(posRepo.Query.Where(p => p.Person_fk == cpr).Count() == 0)
                    {
                        Person per = perRepo.Query.Where(p => p.Cpr == cpr).First();
                        perRepo.Delete(per);
                    }

                    // er adresse i brug?
                }
            }
        }

        private Position Get_Position(Position pos, bool is_new, int opus_id, string position_name, int los_id, string person_cpr,  DateTime ans_dato, DateTime? fra_data, bool is_manager, 
            decimal timetal, int pay_method, string pay_method_text)
        {
            if (is_new)
            {
                pos.Opus_id = opus_id;
            }
            pos.Name = position_name;
            pos.Orgunit_losid_fk = los_id;
            pos.Person_fk = person_cpr;
            pos.Ans_dato = ans_dato;
            pos.Fra_dato = fra_data;
            pos.Is_Manager = is_manager;
            pos.Timetal = timetal;
            pos.Pay_method = pay_method;
            pos.Pay_method_text = pay_method_text;
            pos.Last_changed = DateTime.Now;
            return pos;
        }

        private Person Get_Person(string cpr, string firstname, string lastname, int adr_refid)
        {
            Person res = perRepo.Query.Where(p => p.Cpr.Equals(cpr)).FirstOrDefault();
            if(res == null)
            {
                res = new Person()
                {
                    Cpr = cpr,
                    Firstname = firstname,
                    Lastname = lastname,
                    Name = firstname + " " + lastname,
                    Last_changed = DateTime.Now,
                    Private_adr_fk = adr_refid,
                };
                perRepo.Add(res);
            }
            else
            {
                if (res.Firstname != firstname || res.Lastname != lastname || res.Private_adr_fk != adr_refid)
                {
                    res.Firstname = firstname;
                    res.Lastname = lastname;
                    res.Name = firstname + " " + lastname;
                    res.Private_adr_fk = adr_refid;
                    res.Last_changed = DateTime.Now;
                    perRepo.Update(res);
                }
            }
            return res;
        }

        internal void Add_new_users_to_positions()
        {
            List<int> none_taken_user_opusid = useRepo.Query.Where(u => u.Updated).Select(u => u.Opus_id).ToList<int>();
            foreach(Position pos in posRepo.Query.Where(p => p.User == null)) //&& (p.Orgunit_losid_fk == 1016927 || p.Orgunit_losid_fk == 870650 || p.Orgunit_losid_fk == 1031024 ||
            //p.Orgunit_losid_fk == 822041 || p.Orgunit_losid_fk == 1031023 || p.Orgunit_losid_fk == 822040 || p.Orgunit_losid_fk == 1024926 ||
            //p.Orgunit_losid_fk == 876073 || p.Orgunit_losid_fk == 876074 || p.Orgunit_losid_fk == 1029490 || p.Orgunit_losid_fk == 1012542 ||
            //p.Orgunit_losid_fk == 855183 || p.Orgunit_losid_fk == 846684 || p.Orgunit_losid_fk == 861964 || p.Orgunit_losid_fk == 820579 || 
            //p.Orgunit_losid_fk == 879350 || p.Orgunit_losid_fk == 859357 || p.Orgunit_losid_fk == 859357 || p.Orgunit_losid_fk == 879353 ||
            //p.Orgunit_losid_fk == 1018395 || p.Orgunit_losid_fk == 849926 || p.Orgunit_losid_fk == 849925 || p.Orgunit_losid_fk == 877867 ||
            //p.Orgunit_losid_fk == 877865 || p.Orgunit_losid_fk == 877868 || p.Orgunit_losid_fk == 877872 || p.Orgunit_losid_fk == 877873 ||
            //p.Orgunit_losid_fk == 878190 || p.Orgunit_losid_fk == 1038542 || p.Orgunit_losid_fk == 1049738 || p.Orgunit_losid_fk == 876084 ||
            //p.Orgunit_losid_fk == 877870 || p.Orgunit_losid_fk == 877869 || p.Orgunit_losid_fk == 879349) || p.Orgunit_losid_fk == 879351))
            {
                if (none_taken_user_opusid.Contains(pos.Opus_id))
                {
                    User usr = useRepo.Query.Where(u => u.Opus_id == pos.Opus_id).FirstOrDefault();
                    if (usr != null)
                    {
                        pos.User_fk = usr.Uuid;
                        posRepo.Update(pos);

                        usr.Updated = false;
                        useRepo.Update(usr);

                        queue_user.Add(new qUser()
                        {
                            Change_type = "Created",
                            Opus_id = pos.Opus_id,
                            Time_added = DateTime.Now,
                            Uuid = pos.User.Uuid
                        });
                    }
                }
            }
        }

        // når der sker opdateringer fra AD er de markeret med et updated i dbo.users, dette skal tilføjes til stsorg køen
        internal void Add_updated_users_to_sts_org()
        {
            foreach (User usr in useRepo.Query.Where(u => u.Updated == true)){
                queue_user.Add(new qUser()
                {
                    Change_type = "Updated",
                    Opus_id = usr.Opus_id,
                    Time_added = DateTime.Now,
                    Uuid = usr.Uuid
                });
                usr.Updated = false;
                useRepo.Update(usr);
            }
        }

        internal void Delete_deleted_users()
        {
            foreach(User usr in useRepo.Query.Where(u => u.Deleted_in_ad == true))
            {
                Position pos = posRepo.Query.Where(p => p.User_fk == usr.Uuid).FirstOrDefault();
                if(pos != null)
                {
                    pos.User_fk = null;
                    posRepo.Update(pos);
                    queue_user.Add(new qUser()
                    {
                        Change_type = "Deleted",
                        Opus_id = pos.Opus_id,
                        Time_added = DateTime.Now,
                        Uuid = usr.Uuid
                    });
                }
                useRepo.Delete(usr);
            }
        }

    }
}
