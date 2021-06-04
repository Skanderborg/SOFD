import pyodbc
from datetime import date

class Kmdl2_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_institutions_to_sync(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "SELECT [los_id], \
                        [kmdl2_id], \
                        [parent_orgunit_los_id], \
                        [kmdl2_name], \
                        [longname], \
                        [sync_children] \
                FROM [LORA_SOFD].[kmdl2].[v_institution_to_sync];")
            for row in cursor.fetchall():
                result[row.los_id] = {'los_id' : row.los_id, 'kmdi2_id' : row.kmdl2_id, 'parent_orgunit_los_id' : row.parent_orgunit_los_id,
                'longname' : row.longname, 'sync_children' : row.sync_children}
        return result
    
    def get_dagtilbud(self):
        result = []
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "SELECT [los_id] \
                FROM [LORA_SOFD].[kmdl2].[dagtilbud];")
            for row in cursor.fetchall():
                result.append(row.los_id)
        return result

    def get_employees_in_orgunit(self, los_id):
        result = []
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "EXEC [kmdl2].[get_orgunit_employes] @los_id = ?;", los_id)
            for row in cursor.fetchall():
                result.append({'cpr' : row.cpr, 'firstname' : row.firstname, 'lastname' :  row.lastname, 'title' : row.title,
                'start_date' : row.start_date, 'leave_date' : row.leave_date, 'Email' : row.Email, 'Phone' : row.Phone, 
                'WorkMobile' : row.WorkMobile})
        return result
    '''
    Method used to add RPA to institutions - no longer in use
    def tmp_get_robotos(self):
        result = []
        result.append({'cpr' : self.rpa_ssn, 'firstname' : 'Administrativ', 'lastname' :  'bruger', 'title' : 'administrativ medarbejder',
                'start_date' : date.today(), 'leave_date' : None, 'Email' : 'dof@skanderborg.dk', 'Phone' : '87947000', 
                'WorkMobile' : '87947000'})
        return result
    '''

    def get_orgunit_and_children(self, los_id):
        result = []
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "EXEC [dbo].[get_all_orgunits_below] @Parent = ?;", los_id)
            for row in cursor.fetchall():
                result.append(str(row[0]))
        return result

    def get_kmd_sofd_positiontitle_map(self):
        positiontitle_map = {}
        positiontitle_map['dagtilbudsleder'] = 'institutionManager'
        positiontitle_map['daglig leder'] = 'institutionManager'
        positiontitle_map['daginstitutionsleder'] = 'institutionManager'
        positiontitle_map['leder'] = 'institutionManager'
        positiontitle_map['administrativ leder'] = 'management'
        positiontitle_map['pædagog'] = 'pedagogue'
        positiontitle_map['pædagogmedhjælper'] = 'pedagogue'
        positiontitle_map['pædagogisk assistent'] = 'pedagogue'
        positiontitle_map['pædagogstuderende'] = 'pedagogue'
        positiontitle_map['pædagogmedhjælper-vikar'] = 'pedagogue'
        positiontitle_map['praktikant'] = 'pedagogue'
        positiontitle_map['stedfortræder'] = 'substitute'
        positiontitle_map['ekstern'] = 'consultant'
        positiontitle_map['psykomotorisk terapeut'] = 'consultant'
        positiontitle_map['administrativ medarbejder' ] = 'tAP'
        positiontitle_map['kommunikationsmedarbejder' ] = 'tAP'
        positiontitle_map['ernæringsassistent' ] = 'tAP'
        positiontitle_map['kostfaglig eneansvarlig' ] = 'tAP'
        positiontitle_map['køkkenmedhjælper' ] = 'tAP'
        positiontitle_map['køkkenassistent' ] = 'tAP'
        positiontitle_map['ernæringsassistentelev' ] = 'tAP'
        positiontitle_map['tilkaldevikar-køkkenassistent' ] = 'tAP'
        positiontitle_map['tilkaldevikar-ernæringsassistent' ] = 'tAP'
        positiontitle_map['pb-ernæring' ] = 'tAP'
        positiontitle_map['køkkenmedhjælp' ] = 'tAP'
        positiontitle_map['husassistent' ] = 'tAP'
        positiontitle_map['tilkaldevikar-husassistent' ] = 'tAP'
        positiontitle_map['køkkenleder' ] = 'tAP'
        return positiontitle_map