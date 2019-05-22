using DAL_old;
using DAL_old.LORA_SOFD;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;

namespace Web_app.Services
{
    internal class Sofd_medarbejderoverblik_Service
    {
        private IRepo<v_sofd_medarbejderoverblik> repo = new Sofd_Medarbejderoverblik_Repo(Properties.Settings.Default.lora_sofd_constr);

        internal DataTable Get_Sofd_medarbejderoverblik_DataTable()
        {
            DataTable res = new DataTable();
            res.Columns.Add("Uuid", typeof(string));
            res.Columns.Add("UserId", typeof(string));
            res.Columns.Add("Email", typeof(string));
            res.Columns.Add("Phone", typeof(string));
            res.Columns.Add("WorkMobile", typeof(string));
            res.Columns.Add("person_name", typeof(string));
            res.Columns.Add("Cpr", typeof(string));
            res.Columns.Add("Firstname", typeof(string));
            res.Columns.Add("Lastname", typeof(string));
            res.Columns.Add("privat_gade", typeof(string));
            res.Columns.Add("privat_postnr", typeof(string));
            res.Columns.Add("privat_by", typeof(string));
            res.Columns.Add("Opus_id", typeof(string));
            res.Columns.Add("position_name", typeof(string));
            res.Columns.Add("Ans_dato", typeof(string));
            res.Columns.Add("Fra_dato", typeof(string));
            res.Columns.Add("Is_Manager", typeof(string));
            res.Columns.Add("Timetal", typeof(string));
            res.Columns.Add("Pay_method", typeof(string));
            res.Columns.Add("Pay_method_text", typeof(string));
            res.Columns.Add("User_fk", typeof(string));
            res.Columns.Add("nearmeste_leder", typeof(string));
            res.Columns.Add("orgunit_uuid", typeof(string));
            res.Columns.Add("Los_id", typeof(string));
            res.Columns.Add("org_name", typeof(string));
            res.Columns.Add("PayoutUnitUuid", typeof(string));
            res.Columns.Add("Created_date", typeof(string));
            res.Columns.Add("org_phone", typeof(string));
            res.Columns.Add("org_email", typeof(string));
            res.Columns.Add("Parent_losid", typeof(string));
            res.Columns.Add("Los_short_name", typeof(string));
            res.Columns.Add("org_gade", typeof(string));
            res.Columns.Add("org_postnr", typeof(string));
            res.Columns.Add("org_by", typeof(string));
            res.Columns.Add("Ean", typeof(string));
            res.Columns.Add("Pnr", typeof(string));
            res.Columns.Add("Cost_center", typeof(string));
            res.Columns.Add("Org_type", typeof(string));
            res.Columns.Add("Org_niveau", typeof(string));
            
            foreach (v_sofd_medarbejderoverblik med in repo.Query)
            {
                string uuid = med.Uuid ?? "";
                string UserId = med.UserId ?? "";
                string Email = med.Email ?? "";
                string Phone = med.Phone ?? "";
                string WorkMobile = med.WorkMobile ?? "";
                string person_name = med.person_name;
                string Cpr = med.Cpr;
                string Firstname = med.Firstname;
                string Lastname = med.Lastname;
                string privat_gade = med.privat_gade;
                string privat_postnr = "" + med.privat_postnr;
                string privat_by = med.privat_by;
                string Opus_id = "" + med.Opus_id;
                string position_name = med.position_name;
                string Ans_dato = med.Ans_dato.ToString("dd-MM-yyyy") ?? "";
                string Fra_dato = "";//ToString(this DateTime? dt, string format) ?> DataTable ;
                string Is_Manager = med.Is_Manager.ToString();
                string Timetal = med.Timetal.ToString() ?? "";
                string Pay_method = med.Pay_method.ToString() ?? "";
                string Pay_method_text = "";
                string User_fk = "";
                string nearmeste_leder = "";
                string orgunit_uuid = "";
                string Los_id = "";
                string org_name = "";
                string PayoutUnitUuid = "";
                string Created_date = "";
                string org_phone = "";
                string org_email = "";
                string Parent_losid = "";
                string Los_short_name = "";
                string org_gade = "";
                string org_postnr = "";
                string org_by = "";
                string Ean = "";
                string Pnr = "";
                string Cost_center = "";
                string Org_type = "";
                string Org_niveau = "";

                res.Rows.Add(uuid);
                res.Rows.Add(UserId);
                res.Rows.Add(Email);
                res.Rows.Add(Phone);
                res.Rows.Add(WorkMobile);
                res.Rows.Add(person_name);
                res.Rows.Add(Cpr);
                res.Rows.Add(Firstname);
                res.Rows.Add(Lastname);
                res.Rows.Add(privat_gade);
                res.Rows.Add(privat_postnr);
                res.Rows.Add(privat_by);
                res.Rows.Add(Opus_id);
                res.Rows.Add(position_name);
                res.Rows.Add(Ans_dato);
                res.Rows.Add(Fra_dato);
                res.Rows.Add(Is_Manager);
                res.Rows.Add(Timetal);
                res.Rows.Add(Pay_method);
                res.Rows.Add(Pay_method_text);
                res.Rows.Add(User_fk);
                res.Rows.Add(nearmeste_leder);
                res.Rows.Add(orgunit_uuid);
                res.Rows.Add(Los_id);
                res.Rows.Add(org_name);
                res.Rows.Add(PayoutUnitUuid);
                res.Rows.Add(Created_date);
                res.Rows.Add(org_phone);
                res.Rows.Add(org_email);
                res.Rows.Add(Parent_losid);
                res.Rows.Add(Los_short_name);
                res.Rows.Add(org_gade);
                res.Rows.Add(org_postnr);
                res.Rows.Add(org_by);
                res.Rows.Add(Ean);
                res.Rows.Add(Pnr);
                res.Rows.Add(Cost_center);
                res.Rows.Add(Org_type);
                res.Rows.Add(Org_niveau);
            }

            return res;
        }
    }
}