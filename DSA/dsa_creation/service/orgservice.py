from model.orgunit import Orgunit
import xml.etree.ElementTree as ET


class Orgservice:
    def __init__(self, xmlpath):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()

    def get_orgunits_from_xml(self):
        orgs = []
        for orgunit in self.root.findall('orgUnit'):
            costCenter = None
            if orgunit.find('costCenter') != None:
                costCenter = orgunit.find('costCenter').text

            org = Orgunit(orgunit.get('id'),
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
            orgs.append(org)
        return orgs
