<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="god_ledelse_faelled.aspx.cs" Inherits="Web_app.Views.HR.god_ledelse_faelled" %>

<!DOCTYPE html>

<html>
<head runat="server">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
    <title></title>
    <telerik:RadStyleSheetManager id="RadStyleSheetManager1" runat="server" />
  <style type="text/css">
    .btn-primary {
      background-color: #fdbb33;
      border-color: #fdbb33;
      color: black;
    }
    .btn-primary:hover, .btn-primary:focus, .btn-primary:active, .btn-primary.active, .open>.dropdown-toggle.btn-primary {
      background-color:  #7e676d;
      border-color:  #7e676d;
      color: black;
    }
    body {
      background: #e6ece5;
    }
  </style>
</head>
<body>
  <form id="form1" runat="server">
    <telerik:RadScriptManager ID="RadScriptManager2" runat="server">
      <Scripts>
        <asp:ScriptReference Assembly="Telerik.Web.UI" Name="Telerik.Web.UI.Common.Core.js" />
        <asp:ScriptReference Assembly="Telerik.Web.UI" Name="Telerik.Web.UI.Common.jQuery.js" />
        <asp:ScriptReference Assembly="Telerik.Web.UI" Name="Telerik.Web.UI.Common.jQueryInclude.js" />
      </Scripts>
    </telerik:RadScriptManager>
    <telerik:RadAjaxLoadingPanel runat="server" ID="loadpanel" />

    <div class="container">
    

    </div>

    <telerik:RadAjaxManager ID="RadAjaxManager1" runat="server">
      <AjaxSettings>
        <telerik:AjaxSetting AjaxControlID="btn_add_leder">
          <UpdatedControls>
            <telerik:AjaxUpdatedControl ControlID="gd_leder" LoadingPanelID="loadpanel" />
            <telerik:AjaxUpdatedControl ControlID="cb_beredskabstype" LoadingPanelID="loadpanel" />
            <telerik:AjaxUpdatedControl ControlID="txb_name_leder" LoadingPanelID="loadpanel" />
            <telerik:AjaxUpdatedControl ControlID="txb_mednr_leder" LoadingPanelID="loadpanel" />
            <telerik:AjaxUpdatedControl ControlID="txb_mobil_leder" LoadingPanelID="loadpanel" />
            <telerik:AjaxUpdatedControl ControlID="lbl_success" LoadingPanelID="loadpanel" />
            <telerik:AjaxUpdatedControl ControlID="cb_findmdnr" LoadingPanelID="loadpanel" />
          </UpdatedControls>
        </telerik:AjaxSetting>
      </AjaxSettings>
    </telerik:RadAjaxManager>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>

  </form>
</body>
</html>