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
            res.Columns.Add("Opus_id", typeof(string));
            res.Columns.Add("Firstname", typeof(string));
            res.Columns.Add("Lastname", typeof(string));
            res.Columns.Add("position_name", typeof(string));
            res.Columns.Add("Is_Manager", typeof(string));
            res.Columns.Add("UserId", typeof(string));
            res.Columns.Add("Email", typeof(string));
            res.Columns.Add("Phone", typeof(string));
            res.Columns.Add("WorkMobile", typeof(string));
            res.Columns.Add("Los_id", typeof(string));
            res.Columns.Add("org_name", typeof(string));
            res.Columns.Add("org_gade", typeof(string));
            res.Columns.Add("org_postnr", typeof(string));
            res.Columns.Add("org_by", typeof(string));
            res.Columns.Add("Ean", typeof(string));
            res.Columns.Add("Pnr", typeof(string));
            res.Columns.Add("Cost_center", typeof(string));
            res.Columns.Add("Org_type", typeof(string));
            res.Columns.Add("Org_niveau", typeof(string));
            res.Columns.Add("org_phone", typeof(string));
            res.Columns.Add("org_email", typeof(string));
            res.Columns.Add("Parent_losid", typeof(string));
            res.Columns.Add("Uuid", typeof(string));
            res.Columns.Add("Cpr", typeof(string));
            res.Columns.Add("privat_gade", typeof(string));
            res.Columns.Add("privat_postnr", typeof(string));
            res.Columns.Add("privat_by", typeof(string));
            res.Columns.Add("Ans_dato", typeof(string));
            res.Columns.Add("Fra_dato", typeof(string));
            res.Columns.Add("Timetal", typeof(string));
            res.Columns.Add("Pay_method", typeof(string));
            res.Columns.Add("Pay_method_text", typeof(string));
            res.Columns.Add("nearmeste_leder", typeof(string));
            res.Columns.Add("orgunit_uuid", typeof(string));
            res.Columns.Add("PayoutUnitUuid", typeof(string));
            res.Columns.Add("Created_date", typeof(string));
            res.Columns.Add("Los_short_name", typeof(string));

            
            foreach (v_sofd_medarbejderoverblik med in repo.Query.OrderBy(m => m.Opus_id))
            {
                string Opus_id = "" + med.Opus_id;
                string Firstname = med.Firstname;
                string Lastname = med.Lastname;
                string position_name = med.position_name;
                string Is_Manager = med.Is_Manager.ToString();
                string UserId = med.UserId ?? "Intet AD";
                string Email = med.Email ?? "Intet AD";
                string Phone = med.Phone ?? "Intet AD";
                string WorkMobile = med.WorkMobile ?? "Intet AD";
                string Los_id = med.Los_id.ToString();
                string org_name = med.org_name;
                string org_phone = med.org_phone.ToString() ?? "";
                string org_email = med.org_email ?? "";
                string Parent_losid = med.Parent_losid.ToString();
                string org_gade = med.org_gade ?? "";
                string org_postnr = med.org_postnr.ToString() ?? "";
                string org_by = med.org_by ?? "";
                string Ean = med.Ean.ToString() ?? "";
                string Pnr = med.Pnr.ToString() ?? "";
                string Cost_center = med.Cost_center.ToString() ?? "";
                string Org_type = med.Org_type;
                string Org_niveau = med.Org_niveau.ToString();
                string uuid = med.Uuid ?? "Intet AD";
                string Cpr = med.Cpr;
                string privat_gade = med.privat_gade;
                string privat_postnr = "" + med.privat_postnr;
                string privat_by = med.privat_by;
                string Ans_dato = med.Ans_dato.ToString("dd-MM-yyyy") ?? "";
                string Fra_dato = "";//ToString(this DateTime? dt, string format) ?> DataTable ;
                string Timetal = med.Timetal.ToString() ?? "";
                string Pay_method = med.Pay_method.ToString() ?? "";
                string Pay_method_text = med.Pay_method_text ?? "";
                string nearmeste_leder = med.nearmeste_leder.ToString();
                string orgunit_uuid = med.orgunit_uuid;
                string PayoutUnitUuid = med.PayoutUnitUuid ?? "";
                string Created_date = med.Created_date.ToString("dd-MM-yyyy" ?? "");
                string Los_short_name = med.Los_short_name;

                res.Rows.Add(Opus_id, Firstname, Lastname, position_name, Is_Manager, UserId, Email, Phone, WorkMobile, Los_id, org_name, org_phone, org_email, Parent_losid,
                    org_gade, org_postnr, org_by, Ean, Pnr, Cost_center, Org_type, Org_niveau, uuid, Cpr, privat_gade, privat_postnr, privat_by, Ans_dato, Fra_dato, Timetal, 
                    Pay_method, Pay_method_text, nearmeste_leder, orgunit_uuid, PayoutUnitUuid, Created_date, Los_short_name);
            }

            return res;
        }
    }
}