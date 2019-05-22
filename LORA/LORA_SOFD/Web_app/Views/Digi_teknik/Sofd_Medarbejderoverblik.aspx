<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Sofd_Medarbejderoverblik.aspx.cs" Inherits="Web_app.Views.Digi_teknik.Sofd_Medarbejderoverblik" %>

<html>
<head runat="server">
  <meta charset="utf-8">
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
      <telerik:RadGrid runat="server" ID="sofd_grid" RenderMode="Lightweight" ShowStatusBar="false" AutoGenerateColumns="false" AllowSorting="true"
        AllowMultiRowEdit="false" AllowAutomaticUpdates="true" AllowPaging="true" PageSize="20" OnPreRender="sofd_grid_PreRender">
        <PagerStyle Mode="Slider" Position="Bottom" PageSizeControlType="RadComboBox" />
        <MasterTableView PageSize="20" DataKeyNames="">
          <Columns>
            <telerik:GridBoundColumn UniqueName="" DataField="" HeaderText="" />
          </Columns>
        </MasterTableView>
      </telerik:RadGrid>
    </div>
  </form>
</body>
</html>
