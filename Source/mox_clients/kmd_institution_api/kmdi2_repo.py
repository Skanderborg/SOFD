import pyodbc

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
                        [longname]\
                FROM [LORA_SOFD].[kmdl2].[v_institution_to_sync];")
            for row in cursor.fetchall():
                result[row.los_id] = {'los_id' : row.los_id, 'kmdi2_id' : row.kmdl2_id, 'parent_orgunit_los_id' : row.parent_orgunit_los_id,
                'longname' : row.longname}
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
        positiontitle_map['Dagtilbudsleder'] = 'institutionManager'
        positiontitle_map['Daglig leder'] = 'institutionManager'
        positiontitle_map['Daginstitutionsleder'] = 'institutionManager'
        positiontitle_map['Administrativ leder'] = 'management'
        positiontitle_map['Pædagog'] = 'pedagogue'
        positiontitle_map['Pædagogmedhjælper'] = 'pedagogue'
        positiontitle_map['Pædagogisk assistent'] = 'pedagogue'
        positiontitle_map['Pædagogstuderende'] = 'pedagogue'
        positiontitle_map['Pædagogmedhjælper-vikar'] = 'pedagogue'
        positiontitle_map['Praktikant'] = 'pedagogue'
        positiontitle_map['Stedfortræder'] = 'substitute'
        positiontitle_map['Ekstern'] = 'consultant'
        positiontitle_map['Psykomotorisk terapeut'] = 'consultant'
        positiontitle_map['Administrativ medarbejder' ] = 'tAP'
        positiontitle_map['Kommunikationsmedarbejder' ] = 'tAP'
        positiontitle_map['Ernæringsassistent' ] = 'tAP'
        positiontitle_map['Kostfaglig eneansvarlig' ] = 'tAP'
        positiontitle_map['Køkkenmedhjælper' ] = 'tAP'
        positiontitle_map['Køkkenassistent' ] = 'tAP'
        positiontitle_map['Ernæringsassistentelev' ] = 'tAP'
        positiontitle_map['Tilkaldevikar-Køkkenassistent' ] = 'tAP'
        positiontitle_map['Tilkaldevikar-Ernæringsassistent' ] = 'tAP'
        positiontitle_map['PB-Ernæring' ] = 'tAP'
        positiontitle_map['Køkkenmedhjælp' ] = 'tAP'
        positiontitle_map['Husassistent' ] = 'tAP'
        positiontitle_map['Tilkaldevikar-Husassistent' ] = 'tAP'
        positiontitle_map['Køkkenleder' ] = 'tAP'
        return positiontitle_map