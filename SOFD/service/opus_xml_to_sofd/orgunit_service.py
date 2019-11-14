from model.orgunit import Orgunit
from dal.orgunit_repo import Orgunit_repo
from dal.org_uuid_repo import Org_uuid_repo
import xml.etree.ElementTree as ET
import datetime


class Orgunit_service:
    def __init__(self, xmlpath, constr_lora):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
        self.constr_lora = constr_lora

    def get_orgunits_from_opus_xml(self):
        '''
        OPUS XML filen fra KMD indeholder to tags employee og orgunit.
        Denne funktion danner en dictionary for orgunits.

        Det er los_id som er nøgle.
        Dette er unikt og ændre sig ikke.
        '''
        orgs = {}
        for orgunit in self.root.findall('orgUnit'):
            los_id = orgunit.get('id')
            longname = orgunit.find('longName').text
            # orgunits med # i navnet er nedlagte, og derfor sorterer vi dem fra.
            if '#' in longname:
                continue
            costCenter = None
            if orgunit.find('costCenter') != None:
                costCenter = orgunit.find('costCenter').text

            org = Orgunit(los_id,
                          None,
                          orgunit.get('lastChanged'),
                          longname,
                          orgunit.find('startDate').text,
                          orgunit.find('endDate').text,
                          orgunit.find('parentOrgUnit').text,
                          orgunit.find('shortName').text,
                          orgunit.find('street').text,
                          orgunit.find('zipCode').text,
                          orgunit.find('city').text,
                          orgunit.find('phoneNumber').text,
                          orgunit.find('cvrNr').text,
                          orgunit.find('eanNr').text,
                          orgunit.find('seNr').text,
                          orgunit.find('pNr').text,
                          orgunit.find('orgType').text,
                          orgunit.find('orgTypeTxt').text,
                          None,
                          'opus',
                          None,
                          None,
                          costCenter)
            orgs[int(los_id)] = org
        return orgs

    def update_orgunits(self):
        org_repo = Orgunit_repo(self.constr_lora)
        sofd_orgunits = org_repo.get_orgunits(
            "WHERE [deleted] = 0 and [hierarchy] = 'opus'")
        self.opus_orgunits = Orgunit_service.get_orgunits_from_opus_xml(self)
        orgs_to_update = {}
        orgs_to_insert = {}

        # key er los_id
        for key in self.opus_orgunits:
            opus_org = self.opus_orgunits[key]
            opus_org.niveau = Orgunit_service.get_orgunit_niveau(self, key)
            # top organisationsenheden har ikke en parent, men feltet er not null i DB, derfor dette hack.
            if opus_org.parent_orgunit_los_id is None:
                opus_org.parent_orgunit_los_id = 0

            # hvis en orgunit findes, tjekkes den for forandringer.
            if key in sofd_orgunits:
                sofd_org = sofd_orgunits[key]
                if opus_org.longname == sofd_org.longname and opus_org.startdate == sofd_org.startdate and opus_org.enddate == sofd_org.enddate \
                        and opus_org.parent_orgunit_los_id == sofd_org.parent_orgunit_los_id and opus_org.shortname == sofd_org.shortname and \
                        opus_org.street == sofd_org.street and opus_org.zipcode == sofd_org.zipcode and opus_org.city == sofd_org.city and \
                        opus_org.phonenumber == sofd_org.phonenumber and opus_org.cvr == sofd_org.cvr and opus_org.ean == sofd_org.ean and \
                        opus_org.seNr == sofd_org.seNr and opus_org.pnr == sofd_org.pnr and opus_org.orgtype == sofd_org.orgtype and \
                        opus_org.orgtypetxt == sofd_org.orgtypetxt and opus_org.costcenter == sofd_org.costcenter and \
                        opus_org.niveau == sofd_org.niveau:
                    # er der ikke forandringer, går scriptet videre til næste orgunit
                    continue
                else:
                    orgs_to_update[key] = opus_org

            # ellers indsættes en ny orgunit
            else:
                orgs_to_insert[key] = opus_org

        for los_id in orgs_to_insert:
            org = orgs_to_insert[los_id]
            org.area = Orgunit_service.get_orgunit_area(self, los_id)
            org_repo.insert_orgunit(org)

        for los_id in orgs_to_update:
            org = orgs_to_update[los_id]
            org.area = Orgunit_service.get_orgunit_area(self, los_id)
            org_repo.update_orgunit(org)

        for los_id in sofd_orgunits:
            '''
            Tjekker først om område har ændret sig på orgunits, det forventer vi sjællendt at det gør, men hvis nu
            Derefter slettes orgunits, som ikkel ængere er i OPUS
            '''
            if los_id not in orgs_to_insert and los_id not in orgs_to_update:
                org = sofd_orgunits[los_id]
                current_area = Orgunit_service.get_orgunit_area(self, los_id)
                if org.area != current_area:
                    print('hej')
                    org.area = current_area
                    org_repo.update_orgunit(org)

            # hvis nøglen (los_id) er i SOFD men ikke i OPUS udtræk, er det fordi organisationsenheden er nedlagt
            if los_id not in self.opus_orgunits:
                org_repo.delete_orgunit(los_id)

    def get_orgunit_niveau(self, los_id):
        # Finder en orgunits niveau i org træet, starter ved 1.
        los_id = int(los_id)
        current_org = self.opus_orgunits[los_id]
        if current_org.parent_orgunit_los_id is None or current_org.parent_orgunit_los_id == 0:
            return 1
        else:
            return 1 + Orgunit_service.get_orgunit_niveau(self, current_org.parent_orgunit_los_id)

    def get_orgunit_area(self, los_id):
        los_id = int(los_id)
        current_org = self.opus_orgunits[los_id]
        if current_org.niveau == 5:
            return current_org.longname
        elif current_org.niveau < 5:
            return 'Direktion'
        else:
            return Orgunit_service.get_orgunit_area(self, current_org.parent_orgunit_los_id)

    def set_orgunit_uuid(self):
        uuid_repo = Org_uuid_repo(self.constr_lora)
        org_repo = Orgunit_repo(self.constr_lora)
        uuids = uuid_repo.get_org_uuids()
        orgs = org_repo.get_orgunits(
            "WHERE [new] = 1 and [hierarchy] = 'opus'")
        for key in orgs:
            if key in uuids:
                org = orgs[key]
                org.uuid = uuids[key]
                org_repo.update_orgunit(org)
