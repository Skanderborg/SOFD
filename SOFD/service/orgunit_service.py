from model.orgunit import Orgunit
from dal.orgunit_repo import Orgunit_repo
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
                          costCenter)
            orgs[int(los_id)] = org
        return orgs

    def update_orgunits(self):
        org_repo = Orgunit_repo(self.constr_lora)
        sofd_orgunits = org_repo.get_orgunits(
            "WHERE [deleted] = 0 and [hierarchy] = 'opus'")
        self.opus_orgunits = Orgunit_service.get_orgunits_from_opus_xml(self)

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
                    org_repo.update_orgunit(opus_org)
            # ellers indsættes en ny orgunit
            else:
                org_repo.insert_orgunit(opus_org)

        for key in sofd_orgunits:
            # hvis nøglen (los_id) er i SOFD men ikke i OPUS udtræk, er det fordi organisationsenheden er nedlagt
            if key not in opus_orgunits:
                org_repo.delete_orgunit(key)

    def get_orgunit_niveau(self, los_id):
        los_id = int(los_id)
        current_org = self.opus_orgunits[los_id]
        if current_org.parent_orgunit_los_id is None or current_org.parent_orgunit_los_id == 0:
            return 1
        else:
            return 1 + Orgunit_service.get_orgunit_niveau(self, current_org.parent_orgunit_los_id)
