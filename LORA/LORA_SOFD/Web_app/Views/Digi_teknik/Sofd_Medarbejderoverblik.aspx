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
            <telerik:GridBoundColumn UniqueName="Uuid" DataField="Uuid" HeaderText="Uuid" />
            <telerik:GridBoundColumn UniqueName="UserId" DataField="UserId" HeaderText="UserId" />
            <telerik:GridBoundColumn UniqueName="Email" DataField="Email" HeaderText="Email" />
            <telerik:GridBoundColumn UniqueName="Phone" DataField="Phone" HeaderText="Phone" />
            <telerik:GridBoundColumn UniqueName="WorkMobile" DataField="WorkMobile" HeaderText="WorkMobile" />
            <telerik:GridBoundColumn UniqueName="person_name" DataField="person_name" HeaderText="person_name" />
            <telerik:GridBoundColumn UniqueName="Cpr" DataField="Cpr" HeaderText="Cpr" />
            <telerik:GridBoundColumn UniqueName="Firstname" DataField="Firstname" HeaderText="Firstname" />
            <telerik:GridBoundColumn UniqueName="Lastname" DataField="Lastname" HeaderText="Lastname" />
            <telerik:GridBoundColumn UniqueName="privat_gade" DataField="privat_gade" HeaderText="privat_gade" />
            <telerik:GridBoundColumn UniqueName="privat_postnr" DataField="privat_postnr" HeaderText="privat_postnr" />
            <telerik:GridBoundColumn UniqueName="privat_by" DataField="privat_by" HeaderText="privat_by" />
            <telerik:GridBoundColumn UniqueName="Opus_id" DataField="Opus_id" HeaderText="Opus_id" />
            <telerik:GridBoundColumn UniqueName="position_name" DataField="position_name" HeaderText="position_name" />
            <telerik:GridBoundColumn UniqueName="Ans_dato" DataField="Ans_dato" HeaderText="Ans_dato" />
            <telerik:GridBoundColumn UniqueName="Fra_dato" DataField="Fra_dato" HeaderText="Fra_dato" />
            <telerik:GridBoundColumn UniqueName="Is_Manager" DataField="Is_Manager" HeaderText="Is_Manager" />
            <telerik:GridBoundColumn UniqueName="Timetal" DataField="Timetal" HeaderText="Timetal" />
            <telerik:GridBoundColumn UniqueName="Pay_method" DataField="Pay_method" HeaderText="Pay_method" />
            <telerik:GridBoundColumn UniqueName="Pay_method_text" DataField="Pay_method_text" HeaderText="Pay_method_text" />
            <telerik:GridBoundColumn UniqueName="User_fk" DataField="User_fk" HeaderText="User_fk" />
            <telerik:GridBoundColumn UniqueName="nearmeste_leder" DataField="nearmeste_leder" HeaderText="nearmeste_leder" />
            <telerik:GridBoundColumn UniqueName="orgunit_uuid" DataField="orgunit_uuid" HeaderText="orgunit_uuid" />
            <telerik:GridBoundColumn UniqueName="Los_id" DataField="Los_id" HeaderText="Los_id" />
            <telerik:GridBoundColumn UniqueName="org_name" DataField="org_name" HeaderText="org_name" />
            <telerik:GridBoundColumn UniqueName="PayoutUnitUuid" DataField="PayoutUnitUuid" HeaderText="PayoutUnitUuid" />
            <telerik:GridBoundColumn UniqueName="Created_date" DataField="Created_date" HeaderText="Created_date" />
            <telerik:GridBoundColumn UniqueName="org_phone" DataField="org_phone" HeaderText="org_phone" />
            <telerik:GridBoundColumn UniqueName="org_email" DataField="org_email" HeaderText="org_email" />
            <telerik:GridBoundColumn UniqueName="Parent_losid" DataField="Parent_losid" HeaderText="Parent_losid" />
            <telerik:GridBoundColumn UniqueName="Los_short_name" DataField="Los_short_name" HeaderText="Los_short_name" />
            <telerik:GridBoundColumn UniqueName="org_gade" DataField="org_gade" HeaderText="org_gade" />
            <telerik:GridBoundColumn UniqueName="org_postnr" DataField="org_postnr" HeaderText="org_postnr" />
            <telerik:GridBoundColumn UniqueName="org_by" DataField="org_by" HeaderText="org_by" />
            <telerik:GridBoundColumn UniqueName="Ean" DataField="Ean" HeaderText="Ean" />
            <telerik:GridBoundColumn UniqueName="Pnr" DataField="Pnr" HeaderText="Pnr" />
            <telerik:GridBoundColumn UniqueName="Cost_center" DataField="Cost_center" HeaderText="Cost_center" />
            <telerik:GridBoundColumn UniqueName="Org_type" DataField="Org_type" HeaderText="Org_type" />
            <telerik:GridBoundColumn UniqueName="Org_niveau" DataField="Org_niveau" HeaderText="Org_niveau" />
          </Columns>
        </MasterTableView>
      </telerik:RadGrid>
    </div>
  </form>
</body>
</html>
