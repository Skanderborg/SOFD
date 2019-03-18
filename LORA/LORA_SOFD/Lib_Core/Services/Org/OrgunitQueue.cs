using DAL_old;
using DAL_old.LORA_SOFD;
using Lib_StsOrgSync_mox.Models;
using Lib_StsOrgSync_mox.Services;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Lib_Core.Services.Org
{
    internal class OrgunitQueue
    {
        private IRepo<qOrgunit> queue;
        private IRepo<Orgunit> orgRepo;
        Core_webservice_agent ws;
        string endpoint;

        internal OrgunitQueue(string lora_conStr)
        {
            queue = new QOrgunitRepo(lora_conStr);
        }
        internal OrgunitQueue(string lora_conStr, string api_key, string end_orgunitspoint_url, string cvr)
        {
            queue = new QOrgunitRepo(lora_conStr);
            orgRepo = new OrgunitRepo(lora_conStr);
            endpoint = end_orgunitspoint_url;
            ws = new Core_webservice_agent(api_key, cvr);
        }

        internal void Add_Org_queue_item(string uuid, int los_id, int niveau, string change_type)
        {
            DateTime added_time = DateTime.Now;
            queue.Add(new qOrgunit()
            {
                uuid = uuid,
                los_id = los_id,
                change_type = change_type,
                Niveau = niveau,
                time_changed = added_time
            });
        }

        private void Delete_Qorg_queue_item(int sys_id)
        {
            qOrgunit item = queue.Query.Where(o => o.system_id == sys_id).FirstOrDefault();
            if (item != null)
                queue.Delete(item);
        }

        internal void Handle_creation()
        {
            JsonService js = new JsonService();
            foreach (qOrgunit item in queue.Query.Where(o => o.change_type.Equals("Created")).OrderBy(o => o.time_changed).OrderBy(o => o.Niveau))
            {
                // generate json
                Orgunit_json org_json = Get_Org_Json_obj(item);
                string json = js.Get_orgunit_json(org_json);
                // call web service
                ws.PostOrganisation(json, endpoint);
                // remove from queue
                Delete_Qorg_queue_item(item.system_id);
            }
        }

        internal void Handle_updates()
        {
            JsonService js = new JsonService();
            foreach (qOrgunit item in queue.Query.Where(o => o.change_type.Equals("Updated")).OrderBy(o => o.time_changed).OrderBy(o => o.Niveau))
            {
                // generate json
                Orgunit_json org_json = Get_Org_Json_obj(item);
                string json = js.Get_orgunit_json(org_json);
                // call web service
                ws.PostOrganisation(json, endpoint);
                // remove from queue
                Delete_Qorg_queue_item(item.system_id);
            }
        }

        internal void Handle_Deletes()
        {
            // omvendt order by fordi vi sletter fra bunden
            foreach (qOrgunit item in queue.Query.Where(o => o.change_type.Equals("Deleted")).OrderBy(o => o.time_changed).OrderByDescending(o => o.Niveau))
            {
                // call web serivce
                bool call = ws.DeleteOrganisation(endpoint, item.uuid);
                // remove form queue
                if(call)
                    Delete_Qorg_queue_item(item.system_id);
            }
        }

        private Orgunit_json Get_Org_Json_obj(qOrgunit item)
        {
            Orgunit org = orgRepo.Query.Where(o => o.Los_id == item.los_id).First();
            string _parentOrgUnitUuid = null;
            if (org.Parent_losid != 0)
                _parentOrgUnitUuid = orgRepo.Query.Where(o => o.Los_id == org.Parent_losid).First().Uuid;
            Generic_adress_json _phone = new Generic_adress_json()
            {
                Value = org.Phone
            };
            Generic_adress_json _email = new Generic_adress_json()
            {
                Value = org.Email
            };

            Orgunit_json org_json = new Orgunit_json()
            {
                Uuid = org.Uuid,
                ShortKey = org.Los_id.ToString(),
                Name = org.Name,
                ParentOrgUnitUuid = _parentOrgUnitUuid,
                Timestamp = DateTime.Now,
                Phone = _phone,
                Email = _email,
                ItSystemUuids = new List<string>()
            };

            return org_json;
        }
    }
}
