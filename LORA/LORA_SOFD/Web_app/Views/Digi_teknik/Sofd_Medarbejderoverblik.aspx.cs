using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using Telerik.Web.UI;
using Web_app.Services;

namespace Web_app.Views.Digi_teknik
{
    public partial class Sofd_Medarbejderoverblik : System.Web.UI.Page
    {
        Sofd_medarbejderoverblik_Service service = new Sofd_medarbejderoverblik_Service();
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void sofd_grid_PreRender(object sender, EventArgs e)
        {

        }
    }
}