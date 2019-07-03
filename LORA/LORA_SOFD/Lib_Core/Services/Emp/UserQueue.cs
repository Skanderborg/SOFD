using DAL_old;
using DAL_old.LORA_SOFD;
using Lib_StsOrgSync_mox.Models;
using Lib_StsOrgSync_mox.Services;
using System.Collections.Generic;
using System.Linq;

namespace Lib_Core.Services.Emp
{
    internal class UserQueue
    {
        //private IRepo<User> usr;
        private IRepo<Position> posRepo;
        //private IRepo<Person> per;
        private IRepoQueue<qUser> queue;
        Core_webservice_agent ws;
        string endpoint;

        internal UserQueue(string lora_constr, string api_key, string endpoint_users_url, string cvr)
        {
            //usr = new UserRepo(lora_constr);
            posRepo = new PositionRepo(lora_constr);
            //per = new PersonRepo(lora_constr);
            queue = new QUserRepo(lora_constr);
            endpoint = endpoint_users_url;
            ws = new Core_webservice_agent(api_key, cvr);
        }

        private void Delete_queue_item(qUser item)
        {
            queue.Delete(item);
        }

        internal void Handle_creation()
        {
            JsonService js = new JsonService();
            foreach (qUser item in queue.Query.Where(i => i.Change_type.Equals("Created")))
            {
                // get json
                User_json usr_json = Get_user_json_obj(item);
                string json = js.Get_user_json(usr_json);

                // webservice
                ws.PostUser(json, endpoint);
                //System.IO.File.WriteAllText(@"c:\work\test_user_stsorgsync.json", json);

                // delete from queue
                Delete_queue_item(item);
            }
        }

        internal void Handle_Updates()
        {
            JsonService js = new JsonService();
            foreach (qUser item in queue.Query.Where(i => i.Change_type.Equals("Updated")))
            {
                // get json
                User_json usr_json = Get_user_json_obj(item);
                string json = js.Get_user_json(usr_json);

                // webservice
                ws.PostUser(json, endpoint);
                //System.IO.File.WriteAllText(@"c:\work\test_user_stsorgsync.json", json);

                // delete from queue
                Delete_queue_item(item);
            }
        }

        internal void Handle_Deletes()
        {
            JsonService js = new JsonService();
            foreach (qUser item in queue.Query.Where(i => i.Change_type.Equals("Deleted")))
            {
                // webservice
                // call web serivce
                bool call = ws.DeleteUser(endpoint + "/", item.Uuid);
                // remove form queue
                if (call)
                    Delete_queue_item(item);
            }
        }

        private User_json Get_user_json_obj(qUser item)
        {
            Position pos = posRepo.Query.Where(p => p.Opus_id == item.Opus_id).First();
            Person_json per = new Person_json()
            {
                Name = pos.Person.Name,
                Cpr = pos.Person_fk
            };
            List<Position_json> posses = new List<Position_json>();
            posses.Add(new Position_json()
            {
                Name = pos.Name,
                ShortKey = pos.Opus_id.ToString(),
                OrgUnitUuid = pos.Orgunit.Uuid
            });

            string _email = "";
            if (pos.User.Email != null)
                _email = pos.User.Email;

            Generic_adress_json email = new Generic_adress_json()
            {
                Value = _email
            };

            Generic_adress_json location = new Generic_adress_json()
            {
                Value = pos.Orgunit.Adress.gade
            };

            User_json usr = new User_json()
            {
                Uuid = pos.User.Uuid,
                UserId = pos.User.UserId,
                Email = email,
                Location = location,
                Positions = posses,
                Person = per,
            };
            if (usr.Positions == null)
                throw new System.Exception("usr_position = null");
            return usr;
        }

    }
}
