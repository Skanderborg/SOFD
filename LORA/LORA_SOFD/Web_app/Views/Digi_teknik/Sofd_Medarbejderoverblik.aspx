<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Sofd_Medarbejderoverblik.aspx.cs" Inherits="Web_app.Views.Digi_teknik.Sofd_Medarbejderoverblik" %>

<html>
<head runat="server">
  <meta charset="utf-8">
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
    .container {
      padding: 5px;
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
          AllowMultiRowEdit="false" AllowAutomaticUpdates="true" AllowPaging="true" PageSize="50" OnPreRender="sofd_grid_PreRender" AllowFilteringByColumn="true"
          GroupingSettings-CaseSensitive="false">
          <PagerStyle Mode="Slider" Position="Bottom" PageSizeControlType="RadComboBox"/>
          <MasterTableView PageSize="50" DataKeyNames="Uuid" AllowMultiColumnSorting="true" AllowFilteringByColumn="true">
            <Columns>
              <telerik:GridBoundColumn UniqueName="Opus_id" DataField="Opus_id" HeaderText="Opus_id" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Firstname" DataField="Firstname" HeaderText="Firstname" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Lastname" DataField="Lastname" HeaderText="Lastname" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="position_name" DataField="position_name" HeaderText="position_name" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Is_Manager" DataField="Is_Manager" HeaderText="Is_Manager" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="UserId" DataField="UserId" HeaderText="UserId" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Los_id" DataField="Los_id" HeaderText="Los_id" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="org_name" DataField="org_name" HeaderText="org_name" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Email" DataField="Email" HeaderText="Email" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Phone" DataField="Phone" HeaderText="Phone" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="WorkMobile" DataField="WorkMobile" HeaderText="WorkMobile" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="org_phone" DataField="org_phone" HeaderText="org_phone" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="org_email" DataField="org_email" HeaderText="org_email" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Parent_losid" DataField="Parent_losid" HeaderText="Parent_losid" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="org_gade" DataField="org_gade" HeaderText="org_gade" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="org_postnr" DataField="org_postnr" HeaderText="org_postnr" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="org_by" DataField="org_by" HeaderText="org_by" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Ean" DataField="Ean" HeaderText="Ean" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Pnr" DataField="Pnr" HeaderText="Pnr" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Cost_center" DataField="Cost_center" HeaderText="Cost_center" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Org_type" DataField="Org_type" HeaderText="Org_type" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Org_niveau" DataField="Org_niveau" HeaderText="Org_niveau" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Uuid" DataField="Uuid" HeaderText="Uuid" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Cpr" DataField="Cpr" HeaderText="Cpr" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="privat_gade" DataField="privat_gade" HeaderText="privat_gade" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="privat_postnr" DataField="privat_postnr" HeaderText="privat_postnr" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="privat_by" DataField="privat_by" HeaderText="privat_by" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Ans_dato" DataField="Ans_dato" HeaderText="Ans_dato" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Fra_dato" DataField="Fra_dato" HeaderText="Fra_dato" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Timetal" DataField="Timetal" HeaderText="Timetal" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Pay_method" DataField="Pay_method" HeaderText="Pay_method" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Pay_method_text" DataField="Pay_method_text" HeaderText="Pay_method_text" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="nearmeste_leder" DataField="nearmeste_leder" HeaderText="nearmeste_leder" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="orgunit_uuid" DataField="orgunit_uuid" HeaderText="orgunit_uuid" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="PayoutUnitUuid" DataField="PayoutUnitUuid" HeaderText="PayoutUnitUuid" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Created_date" DataField="Created_date" HeaderText="Created_date" ShowFilterIcon="false" FilterDelay="500" />
              <telerik:GridBoundColumn UniqueName="Los_short_name" DataField="Los_short_name" HeaderText="Los_short_name" ShowFilterIcon="false" FilterDelay="500" />

            </Columns>
          </MasterTableView>
        </telerik:RadGrid>
    </div>

    <telerik:RadAjaxManager ID="RadAjaxManager1" runat="server" EnablePageHeadUpdate="false">
      <AjaxSettings>
        <telerik:AjaxSetting AjaxControlID="sofd_grid">
          <UpdatedControls>
            <telerik:AjaxUpdatedControl ControlID="sofd_grid" LoadingPanelID="loadpanel"/>
          </UpdatedControls>
        </telerik:AjaxSetting>
      </AjaxSettings>
    </telerik:RadAjaxManager>
  </form>
</body>
</html>
