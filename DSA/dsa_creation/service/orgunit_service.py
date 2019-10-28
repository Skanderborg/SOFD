from model.orgunit import Orgunit
from dal.orgunit_repo import Orgunit_repo
import xml.etree.ElementTree as ET


class Orgunit_service:
    def __init__(self, xmlpath, constr_lora):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
        self.constr_lora = constr_lora

    def get_orgunits_from_opus_xml(self):
        orgs = {}
        for orgunit in self.root.findall('orgUnit'):
            costCenter = None
            if orgunit.find('costCenter') != None:
                costCenter = orgunit.find('costCenter').text
            los_id = orgunit.get('id')
            org = Orgunit(los_id,
                          orgunit.get('lastChanged'),
                          orgunit.find('longName').text,
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
                          costCenter)
            orgs[los_id] = org
        return orgs

    def update_orgunits(self):
        org_repo = Orgunit_repo(self.constr_lora)
        sofd_orgunits = org_repo.get_orgunits()
        opus_orgunits = self.get_orgunits_from_opus_xml()

        for key in opus_orgunits:
            opus_org = opus_orgunits[key]
            if opus_org.parent_orgunit_los_id is None:
                opus_org.parent_orgunit_los_id = 0

            if key in sofd_orgunits:
                sofd_org = sofd_orgunits[key]
                if opus_org.longname == sofd_org.longname and opus_org.startdate == sofd_org.startdate and opus_org.enddate == sofd_org.enddate \
                        and opus_org.parent_orgunit_los_id == sofd_org.parent_orgunit_los_id and opus_org.shortname == sofd_org.shortname and \
                        opus_org.street == sofd_org.street and opus_org.zipcode == sofd_org.zipcode and opus_org.city == sofd_org.city and \
                        opus_org.phonenumber == sofd_org.phonenumber and opus_org.cvr == sofd_org.cvr and opus_org.ean == sofd_org.ean and \
                        opus_org.seNr == sofd_org.seNr and opus_org.pnr == sofd_org.pnr and opus_org.orgtype == sofd_org.orgtype and \
                        opus_org.orgtypetxt == sofd_org.orgtypetxt and opus_org.costcenter == sofd_org.costcenter:
                    continue
                else:
                    org_repo.update_orgunits(opus_org)
            else:
                org_repo.insert_orgunit(opus_org)

        for key in sofd_orgunits:
            if key not in opus_orgunits:
                org_repo.delete_orgunit(key)
